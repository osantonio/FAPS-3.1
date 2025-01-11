from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Supply
from datetime import datetime
import os
from werkzeug.utils import secure_filename

supply_bp = Blueprint('supply_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_supply_photo(photo):
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        # Generar nombre único
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        # Asegurar que el directorio existe
        upload_dir = os.path.join('app', 'static', 'uploads', 'supplies')
        os.makedirs(upload_dir, exist_ok=True)
        # Guardar archivo
        photo.save(os.path.join(upload_dir, unique_filename))
        return unique_filename
    return None

@supply_bp.route('/admin/supplies')
def list_supplies():
    supplies = Supply.query.all()
    return render_template('list_supplies.html', supplies=supplies)

@supply_bp.route('/admin/supplies/create', methods=['GET', 'POST'])
def create_supply():
    if request.method == 'POST':
        try:
            name = request.form['name']
            quantity = int(request.form['quantity'])
            category = request.form['category']
            description = request.form.get('description', '')
            
            # Manejar la foto
            photo = request.files.get('photo')
            photo_filename = save_supply_photo(photo) if photo else None
            
            new_supply = Supply(
                name=name,
                quantity=quantity,
                category=category,
                entry_date=datetime.now(),
                description=description,
                photo=photo_filename
            )
            
            db.session.add(new_supply)
            db.session.commit()
            flash('Suministro creado exitosamente', 'success')
            return redirect(url_for('supply_bp.list_supplies'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el suministro: {str(e)}', 'danger')
            
    return render_template('create_supply.html')

@supply_bp.route('/admin/supplies/edit/<int:id>', methods=['GET', 'POST'])
def edit_supply(id):
    supply = Supply.query.get_or_404(id)
    if request.method == 'POST':
        try:
            supply.name = request.form['name']
            supply.quantity = int(request.form['quantity'])
            supply.category = request.form['category']
            supply.description = request.form.get('description', '')
            
            # Manejar la foto
            photo = request.files.get('photo')
            if photo:
                # Si hay una foto anterior, eliminarla
                if supply.photo:
                    old_photo_path = os.path.join('app', 'static', 'uploads', 'supplies', supply.photo)
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                
                # Guardar la nueva foto
                photo_filename = save_supply_photo(photo)
                if photo_filename:
                    supply.photo = photo_filename
            
            db.session.commit()
            flash('Suministro actualizado exitosamente', 'success')
            return redirect(url_for('supply_bp.list_supplies'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el suministro: {str(e)}', 'danger')
            
    return render_template('edit_supply.html', supply=supply)

@supply_bp.route('/admin/supplies/delete/<int:id>', methods=['POST'])
def delete_supply(id):
    try:
        supply = Supply.query.get_or_404(id)
        
        # Eliminar la foto si existe
        if supply.photo:
            photo_path = os.path.join('app', 'static', 'uploads', 'supplies', supply.photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
        
        db.session.delete(supply)
        db.session.commit()
        flash('Suministro eliminado exitosamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el suministro: {str(e)}', 'danger')
        
    return redirect(url_for('supply_bp.list_supplies'))