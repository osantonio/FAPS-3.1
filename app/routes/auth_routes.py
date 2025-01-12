from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from app.extensions import bcrypt
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'admin':
            flash('No tienes permisos para acceder a esta función', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        no_identification = request.form.get('no_identification')
        password = request.form.get('password')
        
        user = User.query.filter_by(no_identification=no_identification).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = user.type_user
            return redirect(url_for('main_bp.dashboard'))
        else:
            flash('Número de identificación o contraseña incorrectos', 'danger')
            return redirect(url_for('auth_bp.login'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth_bp.login')) 