import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# Get the directory where this file is located
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, 'differentiation.db')

def get_db():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with all required tables"""
    conn = get_db()
    cursor = conn.cursor()

    # Users table (teachers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 0,
            gemini_api_key TEXT,
            default_key_requests INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Add is_admin and is_active columns if they don't exist (migration)
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Add API key columns if they don't exist (migration)
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN gemini_api_key TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute('ALTER TABLE users ADD COLUMN default_key_requests INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists

    # API usage tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            endpoint TEXT NOT NULL,
            request_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # User statistics summary table (for quick lookups)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            api_requests_count INTEGER DEFAULT 0,
            lessons_created_count INTEGER DEFAULT 0,
            students_count INTEGER DEFAULT 0,
            groups_count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            accommodations TEXT,
            needs_description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Groups table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Group members junction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
            UNIQUE(group_id, student_id)
        )
    ''')

    # Differentiation sessions (tracks the workflow)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diff_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_material TEXT NOT NULL,
            title TEXT,
            phase TEXT DEFAULT 'analyze',
            suggestions TEXT,
            approved_suggestions TEXT,
            final_content TEXT,
            selected_standards TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Add selected_standards column if it doesn't exist (migration)
    try:
        cursor.execute('ALTER TABLE diff_sessions ADD COLUMN selected_standards TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Session students (which students/groups are involved)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            FOREIGN KEY (session_id) REFERENCES diff_sessions (id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
        )
    ''')

    # Saved lessons (lesson library)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id INTEGER,
            title TEXT NOT NULL,
            original_material TEXT,
            differentiated_content TEXT NOT NULL,
            students_involved TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (session_id) REFERENCES diff_sessions (id) ON DELETE SET NULL
        )
    ''')

    conn.commit()
    conn.close()

def track_api_usage(user_id, endpoint, request_type):
    """Track API usage for statistics"""
    conn = get_db()
    conn.execute(
        'INSERT INTO api_usage (user_id, endpoint, request_type) VALUES (?, ?, ?)',
        (user_id, endpoint, request_type)
    )

    # Update user stats
    conn.execute('''
        INSERT INTO user_stats (user_id, api_requests_count, last_updated)
        VALUES (?, 1, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            api_requests_count = api_requests_count + 1,
            last_updated = CURRENT_TIMESTAMP
    ''', (user_id,))

    conn.commit()
    conn.close()

def update_user_stats(user_id):
    """Update statistics for a user"""
    conn = get_db()

    # Count lessons
    lessons_count = conn.execute(
        'SELECT COUNT(*) as count FROM lessons WHERE user_id = ?', (user_id,)
    ).fetchone()['count']

    # Count students
    students_count = conn.execute(
        'SELECT COUNT(*) as count FROM students WHERE user_id = ?', (user_id,)
    ).fetchone()['count']

    # Count groups
    groups_count = conn.execute(
        'SELECT COUNT(*) as count FROM groups WHERE user_id = ?', (user_id,)
    ).fetchone()['count']

    # Update stats
    conn.execute('''
        INSERT INTO user_stats (user_id, lessons_created_count, students_count, groups_count, last_updated)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            lessons_created_count = ?,
            students_count = ?,
            groups_count = ?,
            last_updated = CURRENT_TIMESTAMP
    ''', (user_id, lessons_count, students_count, groups_count, lessons_count, students_count, groups_count))

    conn.commit()
    conn.close()

def get_user_api_key(user_id):
    """Get user's Gemini API key and default key request count"""
    conn = get_db()
    user = conn.execute(
        'SELECT gemini_api_key, default_key_requests FROM users WHERE id = ?',
        (user_id,)
    ).fetchone()
    conn.close()

    if user:
        return {
            'api_key': user['gemini_api_key'],
            'default_key_requests': user['default_key_requests']
        }
    return None

def save_user_api_key(user_id, api_key):
    """Save user's Gemini API key"""
    conn = get_db()
    conn.execute(
        'UPDATE users SET gemini_api_key = ? WHERE id = ?',
        (api_key, user_id)
    )
    conn.commit()
    conn.close()

def increment_default_key_requests(user_id):
    """Increment the count of requests made with the default API key"""
    conn = get_db()
    conn.execute(
        'UPDATE users SET default_key_requests = default_key_requests + 1 WHERE id = ?',
        (user_id,)
    )
    conn.commit()
    conn.close()

# Initialize database when module is imported
init_db()
