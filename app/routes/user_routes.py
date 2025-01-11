from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db, bcrypt
from app.models import User
from app.routes.auth_routes import login_required
from datetime import datetime
from app.utils import save_profile_photo
import os

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/admin/users')
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)

@user_bp.route('/admin/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
        no_identification = request.form['no_identification']
        password = request.form['password']
        type_user = request.form['type_user']
        email = request.form.get('email')  # Email es opcional

        new_user = User(
            name=name,
            lastname=lastname,
            birthday_date=birthday_date,
            no_identification=no_identification,
            type_user=type_user,
            email=email
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_bp.list_users'))
    return render_template('create_user.html')

@user_bp.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.lastname = request.form['lastname']
        user.birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
        user.no_identification = request.form['no_identification']
        user.type_user = request.form['type_user']
        user.email = request.form.get('email')  # Email es opcional
        if request.form.get('password'):
            user.set_password(request.form['password'])
        db.session.commit()
        return redirect(url_for('user_bp.list_users'))
    return render_template('edit_user.html', user=user)

@user_bp.route('/admin/users/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_bp.list_users'))

@user_bp.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', current_user=user)

@user_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    user = User.query.get(session['user_id'])
    
    # Actualizar información básica
    user.name = request.form['name']
    user.lastname = request.form['lastname']
    user.birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
    
    # Verificar si se está intentando cambiar la contraseña
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if current_password and new_password and confirm_password:
        if not bcrypt.check_password_hash(user.password, current_password):
            flash('La contraseña actual es incorrecta', 'danger')
            return redirect(url_for('user_bp.profile'))
            
        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden', 'danger')
            return redirect(url_for('user_bp.profile'))
            
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        flash('Contraseña actualizada exitosamente', 'success')
    
    try:
        db.session.commit()
        flash('Perfil actualizado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al actualizar el perfil', 'danger')
        
    return redirect(url_for('user_bp.profile'))

@user_bp.route('/profile/update_photo', methods=['POST'])
@login_required
def update_profile_photo():
    if 'photo' not in request.files:
        flash('No se ha seleccionado ningún archivo', 'danger')
        return redirect(url_for('user_bp.profile'))
    
    file = request.files['photo']
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo', 'danger')
        return redirect(url_for('user_bp.profile'))
    
    try:
        user = User.query.get(session['user_id'])
        
        # Si el usuario ya tiene una foto, eliminarla
        if user.profile_photo:
            old_photo_path = os.path.join('app/static', user.profile_photo)
            if os.path.exists(old_photo_path):
                os.remove(old_photo_path)
        
        # Guardar la nueva foto
        photo_path = save_profile_photo(file)
        if photo_path:
            user.profile_photo = photo_path
            db.session.commit()
            flash('Foto de perfil actualizada exitosamente', 'success')
        else:
            flash('Error al guardar la foto. Formato no permitido.', 'danger')
            
    except Exception as e:
        db.session.rollback()
        flash('Error al actualizar la foto de perfil', 'danger')
        print(f"Error: {str(e)}")
    
    return redirect(url_for('user_bp.profile'))
