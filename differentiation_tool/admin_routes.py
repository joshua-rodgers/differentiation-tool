"""
Admin routes for user management and statistics
"""
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from . import db


# This file contains admin routes that will be imported by routes.py
# All routes are defined with the admin_required decorator applied

def admin_dashboard_view():
    """Admin dashboard"""
    conn = db.get_db()

    # Get pending users
    pending_users = conn.execute(
        'SELECT * FROM users WHERE is_active = 0 ORDER BY created_at DESC'
    ).fetchall()

    # Get total users
    total_users = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    active_users = conn.execute('SELECT COUNT(*) as count FROM users WHERE is_active = 1').fetchone()['count']
    admin_users = conn.execute('SELECT COUNT(*) as count FROM users WHERE is_admin = 1').fetchone()['count']

    # Get total lessons
    total_lessons = conn.execute('SELECT COUNT(*) as count FROM lessons').fetchone()['count']

    # Get recent API usage
    recent_api_usage = conn.execute('''
        SELECT COUNT(*) as count, DATE(created_at) as date
        FROM api_usage
        WHERE created_at >= date('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date DESC
    ''').fetchall()

    conn.close()

    return render_template('differentiation_tool/admin/dashboard.html',
                         pending_users=pending_users,
                         total_users=total_users,
                         active_users=active_users,
                         admin_users=admin_users,
                         total_lessons=total_lessons,
                         recent_api_usage=recent_api_usage)


def manage_users_view():
    """List all users"""
    conn = db.get_db()

    search = request.args.get('search', '')
    if search:
        users = conn.execute('''
            SELECT * FROM users
            WHERE email LIKE ? OR first_name LIKE ? OR last_name LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()

    conn.close()

    return render_template('differentiation_tool/admin/manage_users.html',
                         users=users,
                         search=search)


def create_user_view():
    """Create a new user"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        is_admin = 1 if request.form.get('is_admin') else 0
        is_active = 1 if request.form.get('is_active') else 0

        if not all([email, password, first_name, last_name]):
            flash('All fields are required.', 'error')
            return render_template('differentiation_tool/admin/create_user.html')

        conn = db.get_db()

        # Check if user exists
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            flash('Email already registered.', 'error')
            conn.close()
            return render_template('differentiation_tool/admin/create_user.html')

        # Create user
        password_hash = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (email, password_hash, first_name, last_name, is_admin, is_active) VALUES (?, ?, ?, ?, ?, ?)',
            (email, password_hash, first_name, last_name, is_admin, is_active)
        )
        conn.commit()
        conn.close()

        flash('User created successfully!', 'success')
        return redirect(url_for('differentiation.admin_users'))

    return render_template('differentiation_tool/admin/create_user.html')


def edit_user_view(user_id):
    """Edit a user"""
    conn = db.get_db()

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        is_admin = 1 if request.form.get('is_admin') else 0
        is_active = 1 if request.form.get('is_active') else 0
        password = request.form.get('password')

        # Update user
        if password:
            password_hash = generate_password_hash(password)
            conn.execute('''
                UPDATE users SET email = ?, first_name = ?, last_name = ?, is_admin = ?, is_active = ?, password_hash = ?
                WHERE id = ?
            ''', (email, first_name, last_name, is_admin, is_active, password_hash, user_id))
        else:
            conn.execute('''
                UPDATE users SET email = ?, first_name = ?, last_name = ?, is_admin = ?, is_active = ?
                WHERE id = ?
            ''', (email, first_name, last_name, is_admin, is_active, user_id))

        conn.commit()
        conn.close()

        flash('User updated successfully!', 'success')
        return redirect(url_for('differentiation.admin_users'))

    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('differentiation.admin_users'))

    return render_template('differentiation_tool/admin/edit_user.html', user=user)


def delete_user_view(user_id):
    """Delete a user"""
    # Prevent deleting yourself
    if user_id == session['user_id']:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('differentiation.admin_users'))

    conn = db.get_db()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

    flash('User deleted successfully!', 'success')
    return redirect(url_for('differentiation.admin_users'))


def bulk_delete_users_view():
    """Bulk delete users"""
    user_ids = request.form.getlist('user_ids')

    if not user_ids:
        flash('No users selected.', 'warning')
        return redirect(url_for('differentiation.admin_users'))

    # Prevent deleting yourself
    if str(session['user_id']) in user_ids:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('differentiation.admin_users'))

    conn = db.get_db()

    for user_id in user_ids:
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))

    conn.commit()
    conn.close()

    flash(f'{len(user_ids)} user(s) deleted successfully!', 'success')
    return redirect(url_for('differentiation.admin_users'))


def approve_user_view(user_id):
    """Approve/activate a user"""
    conn = db.get_db()
    conn.execute('UPDATE users SET is_active = 1 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

    flash('User approved successfully!', 'success')
    return redirect(url_for('differentiation.admin_dashboard'))


def statistics_view():
    """View detailed statistics"""
    conn = db.get_db()

    # Get all users with their stats
    users_stats = conn.execute('''
        SELECT u.id, u.email, u.first_name, u.last_name, u.is_admin, u.is_active, u.created_at,
               COALESCE(s.api_requests_count, 0) as api_requests,
               COALESCE(s.lessons_created_count, 0) as lessons_created,
               COALESCE(s.students_count, 0) as students_count,
               COALESCE(s.groups_count, 0) as groups_count
        FROM users u
        LEFT JOIN user_stats s ON u.id = s.user_id
        ORDER BY api_requests DESC
    ''').fetchall()

    # Get API usage over time
    api_usage_timeline = conn.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM api_usage
        WHERE created_at >= date('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date DESC
    ''').fetchall()

    # Get top API users
    top_api_users = conn.execute('''
        SELECT u.first_name, u.last_name, u.email, COUNT(a.id) as api_count
        FROM users u
        JOIN api_usage a ON u.id = a.user_id
        GROUP BY u.id
        ORDER BY api_count DESC
        LIMIT 10
    ''').fetchall()

    # Get lessons created over time
    lessons_timeline = conn.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM lessons
        WHERE created_at >= date('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date DESC
    ''').fetchall()

    conn.close()

    return render_template('differentiation_tool/admin/statistics.html',
                         users_stats=users_stats,
                         api_usage_timeline=api_usage_timeline,
                         top_api_users=top_api_users,
                         lessons_timeline=lessons_timeline)
