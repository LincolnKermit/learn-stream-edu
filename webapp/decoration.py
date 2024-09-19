from functools import wraps
from flask import flash, redirect, session, url_for
from py.config.model import User


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session and session.get('right') == 'admin':
            return f(*args, **kwargs)
        else:
            flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'error')
            return redirect(url_for('users.login'))
    return decorated_function


def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Vous devez être connecté pour accéder à cette page.")
            return redirect(url_for('users.login'))
        
        user = User.query.filter_by(username=session['username']).first()
        if user.right == 'admin':
            return f(*args, **kwargs)

        if not user or user.right != 'student':
            flash("Vous n'avez pas les autorisations nécessaires pour accéder à cette page.")
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function