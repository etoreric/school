from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def admin_required(f):
    """Restrict access to admin users only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
