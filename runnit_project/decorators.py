from functools import wraps
from flask import session,url_for,redirect,flash


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if not "user_id" in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if not user.is_admin:
            flash('You do not have permission to perform this action.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  # Checking if the user is logged in
            flash('You need to be logged in to access this page.', 'warning')
            return redirect(url_for('login'))  # Redirect to the login page
        return f(*args, **kwargs)  # Proceed if the user is logged in
    return decorated_function
