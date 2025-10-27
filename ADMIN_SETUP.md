# Admin Setup Guide

## Creating the First Admin User

Since the app requires admin approval for new accounts, you need to manually create the first admin user directly in the database.

### Option 1: Using Python Script (Recommended)

Create and run this Python script in your project directory:

```python
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
```

Run it:
```bash
python create_admin.py
```

### Option 2: Using SQLite Command Line

1. Open the database:
```bash
sqlite3 differentiation_tool/differentiation.db
```

2. Generate a password hash (you'll need to do this in Python first):
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("your-password-here"))
```

3. Insert the admin user:
```sql
INSERT INTO users (email, password_hash, first_name, last_name, is_admin, is_active)
VALUES ('admin@example.com', 'paste-hashed-password-here', 'Admin', 'User', 1, 1);
```

4. Exit SQLite:
```sql
.exit
```

### Option 3: Temporarily Modify Signup (Development Only)

For development/testing, you can temporarily modify the signup process:

1. Edit `differentiation_tool/routes.py`
2. In the `signup()` function, temporarily change line 79 to:
   ```python
   'INSERT INTO users (email, password_hash, first_name, last_name, is_admin, is_active) VALUES (?, ?, ?, ?, 1, 1)',
   ```
3. Sign up through the web interface
4. **IMMEDIATELY** revert the changes to prevent security issues

## Admin Features

Once logged in as admin, you can:

- **Approve new user accounts** from the admin dashboard
- **Manage users**: Create, edit, delete, and change user permissions
- **Promote users to admin** by editing their account
- **Bulk delete users** from the user management page
- **View statistics**: Track API usage, lessons created, and user activity
- **Change passwords** for any user

## Admin Dashboard Access

After logging in as an admin, you'll see an "Admin" link (in orange) in the navigation bar. Click it to access:

- **Admin Dashboard**: Pending approvals and quick stats
- **Manage Users**: Full user management interface
- **Statistics**: Detailed usage analytics

## Security Notes

1. **Change the default admin password** immediately after first login
2. **Use strong passwords** for all admin accounts
3. **Limit admin accounts** to trusted personnel only
4. **Regular backups** of the database are recommended
5. **Review pending accounts** regularly to prevent unauthorized access

## Approving New Users

When new users sign up:

1. They'll see a message that their account is pending approval
2. You'll see them in the "Pending User Approvals" section of the admin dashboard
3. Click "Approve" to activate their account
4. They'll then be able to log in
5. You can also "Reject" (delete) accounts if needed

## User Types

- **Regular User**: Can create students, groups, and differentiated lessons
- **Admin**: Has all user capabilities PLUS can manage other users and view statistics
