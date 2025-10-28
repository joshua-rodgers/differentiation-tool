# create_admin.py
import sqlite3
from werkzeug.security import generate_password_hash

# Update these values
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "your-secure-password-here"
ADMIN_FIRST_NAME = "Admin"
ADMIN_LAST_NAME = "User"

# Path to database
DB_PATH = "differentiation_tool/differentiation.db"

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create admin user
password_hash = generate_password_hash(ADMIN_PASSWORD)
cursor.execute('''
    INSERT INTO users (email, password_hash, first_name, last_name, is_admin, is_active)
    VALUES (?, ?, ?, ?, 1, 1)
''', (ADMIN_EMAIL, password_hash, ADMIN_FIRST_NAME, ADMIN_LAST_NAME))

conn.commit()
conn.close()

print(f"Admin user created successfully!")
print(f"Email: {ADMIN_EMAIL}")
print(f"You can now log in with these credentials.")