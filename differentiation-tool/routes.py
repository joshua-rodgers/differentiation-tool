from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json
from datetime import datetime

from . import db
from . import gemini_api

bp = Blueprint('differentiation', __name__,
               template_folder='templates',
               static_folder='static',
               url_prefix='/differentiation')

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('differentiation.login'))
        return f(*args, **kwargs)
    return decorated_function

# ============= LANDING AND AUTH ROUTES =============

@bp.route('/')
def landing():
    """Landing page"""
    if 'user_id' in session:
        return redirect(url_for('differentiation.dashboard'))
    return render_template('differentiation-tool/landing.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Teacher signup"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        # Validate
        if not all([email, password, first_name, last_name]):
            flash('All fields are required.', 'error')
            return render_template('differentiation-tool/signup.html')

        # Check if user exists
        conn = db.get_db()
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            flash('Email already registered.', 'error')
            conn.close()
            return render_template('differentiation-tool/signup.html')

        # Create user
        password_hash = generate_password_hash(password)
        cursor = conn.execute(
            'INSERT INTO users (email, password_hash, first_name, last_name) VALUES (?, ?, ?, ?)',
            (email, password_hash, first_name, last_name)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        # Log in
        session['user_id'] = user_id
        session['user_name'] = f"{first_name} {last_name}"
        flash('Account created successfully!', 'success')
        return redirect(url_for('differentiation.dashboard'))

    return render_template('differentiation-tool/signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Teacher login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = db.get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = f"{user['first_name']} {user['last_name']}"
            flash('Logged in successfully!', 'success')
            return redirect(url_for('differentiation.dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('differentiation-tool/login.html')

@bp.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('differentiation.landing'))

# ============= DASHBOARD =============

@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    user_id = session['user_id']
    conn = db.get_db()

    # Get counts
    student_count = conn.execute('SELECT COUNT(*) as count FROM students WHERE user_id = ?', (user_id,)).fetchone()['count']
    group_count = conn.execute('SELECT COUNT(*) as count FROM groups WHERE user_id = ?', (user_id,)).fetchone()['count']
    lesson_count = conn.execute('SELECT COUNT(*) as count FROM lessons WHERE user_id = ?', (user_id,)).fetchone()['count']

    # Get recent lessons
    recent_lessons = conn.execute(
        'SELECT * FROM lessons WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
        (user_id,)
    ).fetchall()

    # Get active sessions
    active_sessions = conn.execute(
        'SELECT * FROM diff_sessions WHERE user_id = ? AND phase != "completed" ORDER BY updated_at DESC',
        (user_id,)
    ).fetchall()

    conn.close()

    return render_template('differentiation-tool/dashboard.html',
                         student_count=student_count,
                         group_count=group_count,
                         lesson_count=lesson_count,
                         recent_lessons=recent_lessons,
                         active_sessions=active_sessions)

# ============= STUDENT MANAGEMENT =============

@bp.route('/students')
@login_required
def students():
    """List all students"""
    user_id = session['user_id']
    conn = db.get_db()
    students = conn.execute(
        'SELECT * FROM students WHERE user_id = ? ORDER BY last_name, first_name',
        (user_id,)
    ).fetchall()
    conn.close()
    return render_template('differentiation-tool/students.html', students=students)

@bp.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """Add a new student"""
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        accommodations = request.form.get('accommodations')
        needs_description = request.form.get('needs_description')

        if not first_name or not last_name:
            flash('First and last name are required.', 'error')
            return render_template('differentiation-tool/add_student.html')

        conn = db.get_db()
        conn.execute(
            'INSERT INTO students (user_id, first_name, last_name, accommodations, needs_description) VALUES (?, ?, ?, ?, ?)',
            (session['user_id'], first_name, last_name, accommodations, needs_description)
        )
        conn.commit()
        conn.close()

        flash('Student added successfully!', 'success')
        return redirect(url_for('differentiation.students'))

    return render_template('differentiation-tool/add_student.html')

@bp.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    """Edit a student"""
    user_id = session['user_id']
    conn = db.get_db()

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        accommodations = request.form.get('accommodations')
        needs_description = request.form.get('needs_description')

        conn.execute(
            'UPDATE students SET first_name = ?, last_name = ?, accommodations = ?, needs_description = ? WHERE id = ? AND user_id = ?',
            (first_name, last_name, accommodations, needs_description, student_id, user_id)
        )
        conn.commit()
        conn.close()

        flash('Student updated successfully!', 'success')
        return redirect(url_for('differentiation.students'))

    student = conn.execute('SELECT * FROM students WHERE id = ? AND user_id = ?', (student_id, user_id)).fetchone()
    conn.close()

    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('differentiation.students'))

    return render_template('differentiation-tool/edit_student.html', student=student)

@bp.route('/students/delete/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    """Delete a student"""
    conn = db.get_db()
    conn.execute('DELETE FROM students WHERE id = ? AND user_id = ?', (student_id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('differentiation.students'))

# ============= GROUP MANAGEMENT =============

@bp.route('/groups')
@login_required
def groups():
    """List all groups"""
    user_id = session['user_id']
    conn = db.get_db()

    # Get groups with member counts
    groups = conn.execute('''
        SELECT g.*, COUNT(gm.student_id) as member_count
        FROM groups g
        LEFT JOIN group_members gm ON g.id = gm.group_id
        WHERE g.user_id = ?
        GROUP BY g.id
        ORDER BY g.name
    ''', (user_id,)).fetchall()

    conn.close()
    return render_template('differentiation-tool/groups.html', groups=groups)

@bp.route('/groups/add', methods=['GET', 'POST'])
@login_required
def add_group():
    """Add a new group"""
    user_id = session['user_id']
    conn = db.get_db()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        student_ids = request.form.getlist('students')

        if not name:
            flash('Group name is required.', 'error')
        else:
            cursor = conn.execute(
                'INSERT INTO groups (user_id, name, description) VALUES (?, ?, ?)',
                (user_id, name, description)
            )
            group_id = cursor.lastrowid

            # Add members
            for student_id in student_ids:
                conn.execute(
                    'INSERT INTO group_members (group_id, student_id) VALUES (?, ?)',
                    (group_id, student_id)
                )

            conn.commit()
            conn.close()
            flash('Group created successfully!', 'success')
            return redirect(url_for('differentiation.groups'))

    # Get all students for the form
    students = conn.execute(
        'SELECT * FROM students WHERE user_id = ? ORDER BY last_name, first_name',
        (user_id,)
    ).fetchall()
    conn.close()

    return render_template('differentiation-tool/add_group.html', students=students)

@bp.route('/groups/edit/<int:group_id>', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    """Edit a group"""
    user_id = session['user_id']
    conn = db.get_db()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        student_ids = request.form.getlist('students')

        conn.execute(
            'UPDATE groups SET name = ?, description = ? WHERE id = ? AND user_id = ?',
            (name, description, group_id, user_id)
        )

        # Update members - delete all and re-add
        conn.execute('DELETE FROM group_members WHERE group_id = ?', (group_id,))
        for student_id in student_ids:
            conn.execute(
                'INSERT INTO group_members (group_id, student_id) VALUES (?, ?)',
                (group_id, student_id)
            )

        conn.commit()
        conn.close()
        flash('Group updated successfully!', 'success')
        return redirect(url_for('differentiation.groups'))

    # Get group
    group = conn.execute('SELECT * FROM groups WHERE id = ? AND user_id = ?', (group_id, user_id)).fetchone()
    if not group:
        flash('Group not found.', 'error')
        conn.close()
        return redirect(url_for('differentiation.groups'))

    # Get all students
    students = conn.execute(
        'SELECT * FROM students WHERE user_id = ? ORDER BY last_name, first_name',
        (user_id,)
    ).fetchall()

    # Get current members
    member_ids = [row['student_id'] for row in conn.execute(
        'SELECT student_id FROM group_members WHERE group_id = ?', (group_id,)
    ).fetchall()]

    conn.close()

    return render_template('differentiation-tool/edit_group.html',
                         group=group, students=students, member_ids=member_ids)

@bp.route('/groups/delete/<int:group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    """Delete a group"""
    conn = db.get_db()
    conn.execute('DELETE FROM groups WHERE id = ? AND user_id = ?', (group_id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Group deleted successfully!', 'success')
    return redirect(url_for('differentiation.groups'))

# ============= DIFFERENTIATION WORKFLOW =============

@bp.route('/differentiate/new', methods=['GET', 'POST'])
@login_required
def new_differentiation():
    """Phase 1: Input material and select students"""
    user_id = session['user_id']
    conn = db.get_db()

    if request.method == 'POST':
        title = request.form.get('title')
        material = request.form.get('material')
        selected_students = request.form.getlist('students')
        selected_groups = request.form.getlist('groups')

        if not material:
            flash('Please enter the lesson material.', 'error')
        elif not selected_students and not selected_groups:
            flash('Please select at least one student or group.', 'error')
        else:
            # Create session
            cursor = conn.execute(
                'INSERT INTO diff_sessions (user_id, original_material, title, phase) VALUES (?, ?, ?, ?)',
                (user_id, material, title, 'select_students')
            )
            session_id = cursor.lastrowid

            # Add selected students
            all_student_ids = set(selected_students)

            # Add students from groups
            for group_id in selected_groups:
                member_ids = conn.execute(
                    'SELECT student_id FROM group_members WHERE group_id = ?', (group_id,)
                ).fetchall()
                all_student_ids.update([str(row['student_id']) for row in member_ids])

            # Insert into session_students
            for student_id in all_student_ids:
                conn.execute(
                    'INSERT INTO session_students (session_id, student_id) VALUES (?, ?)',
                    (session_id, student_id)
                )

            conn.commit()
            conn.close()

            return redirect(url_for('differentiation.generate_suggestions', session_id=session_id))

    # Get students and groups
    students = conn.execute(
        'SELECT * FROM students WHERE user_id = ? ORDER BY last_name, first_name',
        (user_id,)
    ).fetchall()

    groups = conn.execute(
        'SELECT g.*, COUNT(gm.student_id) as member_count FROM groups g LEFT JOIN group_members gm ON g.id = gm.group_id WHERE g.user_id = ? GROUP BY g.id ORDER BY g.name',
        (user_id,)
    ).fetchall()

    conn.close()

    return render_template('differentiation-tool/new_differentiation.html',
                         students=students, groups=groups)

@bp.route('/differentiate/<int:session_id>/suggestions')
@login_required
def generate_suggestions(session_id):
    """Phase 2: Generate suggestions using Gemini"""
    user_id = session['user_id']
    conn = db.get_db()

    # Get session
    sess = conn.execute(
        'SELECT * FROM diff_sessions WHERE id = ? AND user_id = ?',
        (session_id, user_id)
    ).fetchone()

    if not sess:
        flash('Session not found.', 'error')
        conn.close()
        return redirect(url_for('differentiation.dashboard'))

    # Get students involved
    students = conn.execute('''
        SELECT s.* FROM students s
        JOIN session_students ss ON s.id = ss.student_id
        WHERE ss.session_id = ?
    ''', (session_id,)).fetchall()

    # Prepare student data
    students_data = []
    for student in students:
        students_data.append({
            'name': f"{student['first_name']} {student['last_name']}",
            'accommodations': student['accommodations'] or '',
            'needs': student['needs_description'] or ''
        })

    # Generate suggestions if not already done
    if not sess['suggestions']:
        try:
            suggestions = gemini_api.generate_suggestions(
                sess['original_material'],
                students_data
            )
            suggestions_json = json.dumps(suggestions)

            conn.execute(
                'UPDATE diff_sessions SET suggestions = ?, phase = ? WHERE id = ?',
                (suggestions_json, 'review_suggestions', session_id)
            )
            conn.commit()
        except Exception as e:
            flash(f'Error generating suggestions: {str(e)}', 'error')
            suggestions = []
            suggestions_json = '[]'
    else:
        suggestions_json = sess['suggestions']
        suggestions = json.loads(suggestions_json)

    conn.close()

    return render_template('differentiation-tool/suggestions.html',
                         session_id=session_id,
                         session=sess,
                         suggestions=suggestions,
                         students=students)

@bp.route('/differentiate/<int:session_id>/refine', methods=['POST'])
@login_required
def refine_suggestions(session_id):
    """Phase 3: Refine suggestions"""
    user_id = session['user_id']
    approved = request.form.getlist('approved')

    conn = db.get_db()
    sess = conn.execute(
        'SELECT * FROM diff_sessions WHERE id = ? AND user_id = ?',
        (session_id, user_id)
    ).fetchone()

    if not sess:
        flash('Session not found.', 'error')
        conn.close()
        return redirect(url_for('differentiation.dashboard'))

    # Get all suggestions
    all_suggestions = json.loads(sess['suggestions'])

    # Filter to approved ones
    approved_suggestions = [all_suggestions[int(i)] for i in approved]

    conn.execute(
        'UPDATE diff_sessions SET approved_suggestions = ?, phase = ? WHERE id = ?',
        (json.dumps(approved_suggestions), 'ready_to_generate', session_id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('differentiation.generate_final', session_id=session_id))

@bp.route('/differentiate/<int:session_id>/generate')
@login_required
def generate_final(session_id):
    """Phase 4: Generate final differentiated content"""
    user_id = session['user_id']
    conn = db.get_db()

    sess = conn.execute(
        'SELECT * FROM diff_sessions WHERE id = ? AND user_id = ?',
        (session_id, user_id)
    ).fetchone()

    if not sess:
        flash('Session not found.', 'error')
        conn.close()
        return redirect(url_for('differentiation.dashboard'))

    # Generate content if not already done
    if not sess['final_content']:
        approved_suggestions = json.loads(sess['approved_suggestions'])
        suggestion_texts = [s['text'] for s in approved_suggestions]

        try:
            final_content = gemini_api.generate_differentiated_content(
                sess['original_material'],
                suggestion_texts
            )

            conn.execute(
                'UPDATE diff_sessions SET final_content = ?, phase = ?, updated_at = ? WHERE id = ?',
                (final_content, 'completed', datetime.now(), session_id)
            )
            conn.commit()
        except Exception as e:
            flash(f'Error generating content: {str(e)}', 'error')
            final_content = f"Error: {str(e)}"
    else:
        final_content = sess['final_content']

    conn.close()

    return render_template('differentiation-tool/final_content.html',
                         session_id=session_id,
                         session=sess,
                         final_content=final_content)

@bp.route('/differentiate/<int:session_id>/save', methods=['POST'])
@login_required
def save_to_library(session_id):
    """Save differentiated lesson to library"""
    user_id = session['user_id']
    conn = db.get_db()

    sess = conn.execute(
        'SELECT * FROM diff_sessions WHERE id = ? AND user_id = ?',
        (session_id, user_id)
    ).fetchone()

    if not sess:
        flash('Session not found.', 'error')
        conn.close()
        return redirect(url_for('differentiation.dashboard'))

    # Get students involved
    students = conn.execute('''
        SELECT s.first_name, s.last_name FROM students s
        JOIN session_students ss ON s.id = ss.student_id
        WHERE ss.session_id = ?
    ''', (session_id,)).fetchall()

    students_text = ', '.join([f"{s['first_name']} {s['last_name']}" for s in students])

    # Save to library
    conn.execute('''
        INSERT INTO lessons (user_id, session_id, title, original_material, differentiated_content, students_involved)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, session_id, sess['title'], sess['original_material'], sess['final_content'], students_text))

    conn.commit()
    conn.close()

    flash('Lesson saved to your library!', 'success')
    return redirect(url_for('differentiation.lesson_library'))

# ============= LESSON LIBRARY =============

@bp.route('/library')
@login_required
def lesson_library():
    """View saved lessons"""
    user_id = session['user_id']
    conn = db.get_db()

    lessons = conn.execute(
        'SELECT * FROM lessons WHERE user_id = ? ORDER BY created_at DESC',
        (user_id,)
    ).fetchall()

    conn.close()

    return render_template('differentiation-tool/library.html', lessons=lessons)

@bp.route('/library/<int:lesson_id>')
@login_required
def view_lesson(lesson_id):
    """View a specific lesson"""
    user_id = session['user_id']
    conn = db.get_db()

    lesson = conn.execute(
        'SELECT * FROM lessons WHERE id = ? AND user_id = ?',
        (lesson_id, user_id)
    ).fetchone()

    conn.close()

    if not lesson:
        flash('Lesson not found.', 'error')
        return redirect(url_for('differentiation.lesson_library'))

    return render_template('differentiation-tool/view_lesson.html', lesson=lesson)

@bp.route('/library/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    """Delete a lesson"""
    conn = db.get_db()
    conn.execute('DELETE FROM lessons WHERE id = ? AND user_id = ?', (lesson_id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Lesson deleted successfully!', 'success')
    return redirect(url_for('differentiation.lesson_library'))
