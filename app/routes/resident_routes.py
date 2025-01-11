from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db, bcrypt
from app.models import Resident, User
from datetime import datetime
from app.routes.auth_routes import login_required, admin_required
from app.utils import save_profile_photo
import os

resident_bp = Blueprint('resident_bp', __name__)

@resident_bp.route('/admin/residents')
@login_required
def list_residents():
    residents = Resident.query.all()
    # Obtener los usuarios asociados a cada residente
    resident_users = {}
    for resident in residents:
        user = User.query.filter_by(no_identification=resident.no_identification).first()
        resident_users[resident.id] = user
    return render_template('list_residents.html', 
                         residents=residents, 
                         resident_users=resident_users,
                         is_admin=(session.get('user_type') == 'admin'))

@resident_bp.route('/admin/residents/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_resident():
    if request.method == 'POST':
        try:
            # Datos del residente
            name = request.form['name']
            lastname = request.form['lastname']
            birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
            no_identification = request.form['no_identification']
            health_status = request.form['health_status']
            medical_conditions = request.form['medical_conditions']
            medications = request.form['medications']
            medical_history = request.form['medical_history']
            special_requirements = request.form['special_requirements']

            # Crear el residente
            new_resident = Resident(
                name=name,
                lastname=lastname,
                birthday_date=birthday_date,
                no_identification=no_identification,
                health_status=health_status,
                medical_conditions=medical_conditions,
                medications=medications,
                medical_history=medical_history,
                special_requirements=special_requirements
            )

            # Guardar el registro del residente
            db.session.add(new_resident)
            db.session.commit()

            flash('Residente creado exitosamente', 'success')
            return redirect(url_for('resident_bp.list_residents'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el residente: {str(e)}', 'danger')
            return redirect(url_for('resident_bp.create_resident'))

    return render_template('create_resident.html')

@resident_bp.route('/admin/residents/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_resident(id):
    resident = Resident.query.get_or_404(id)
    user = User.query.filter_by(no_identification=resident.no_identification).first()

    if request.method == 'POST':
        try:
            # Actualizar datos del residente
            resident.name = request.form['name']
            resident.lastname = request.form['lastname']
            resident.birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
            resident.health_status = request.form['health_status']
            resident.medical_conditions = request.form['medical_conditions']
            resident.medications = request.form['medications']
            resident.medical_history = request.form['medical_history']
            resident.special_requirements = request.form['special_requirements']

            # Actualizar datos del usuario si existe
            if user:
                user.name = request.form['name']
                user.lastname = request.form['lastname']
                user.birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
                
                # Actualizar contraseña si se proporcionó una nueva
                new_password = request.form.get('password')
                if new_password:
                    user.set_password(new_password)

                # Actualizar foto si se proporcionó una nueva
                if 'profile_photo' in request.files:
                    file = request.files['profile_photo']
                    if file and file.filename != '':
                        # Eliminar foto anterior si existe
                        if user.profile_photo:
                            old_photo_path = os.path.join('app/static', user.profile_photo)
                            if os.path.exists(old_photo_path):
                                os.remove(old_photo_path)
                        
                        # Guardar nueva foto
                        photo_path = save_profile_photo(file)
                        if photo_path:
                            user.profile_photo = photo_path

            db.session.commit()
            flash('Residente actualizado exitosamente', 'success')
            return redirect(url_for('resident_bp.list_residents'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el residente: {str(e)}', 'danger')

    return render_template('edit_resident.html', resident=resident, user=user)

@resident_bp.route('/admin/residents/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_resident(id):
    try:
        resident = Resident.query.get_or_404(id)
        user = User.query.filter_by(no_identification=resident.no_identification).first()

        # Eliminar la foto de perfil si existe
        if user and user.profile_photo:
            photo_path = os.path.join('app/static', user.profile_photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)

        # Eliminar el usuario y el residente
        if user:
            db.session.delete(user)
        db.session.delete(resident)
        db.session.commit()

        flash('Residente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el residente: {str(e)}', 'danger')

    return redirect(url_for('resident_bp.list_residents'))