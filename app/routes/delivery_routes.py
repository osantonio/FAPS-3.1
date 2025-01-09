from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import Delivery, Supply, Resident, delivery_supplies
from datetime import datetime

delivery_bp = Blueprint('delivery_bp', __name__)

@delivery_bp.route('/admin/deliveries')
def list_deliveries():
    deliveries = Delivery.query.all()
    return render_template('list_deliveries.html', deliveries=deliveries)

@delivery_bp.route('/admin/deliveries/create', methods=['GET', 'POST'])
def create_delivery():
    if request.method == 'POST':
        try:
            supply_id = request.form['supply_id']
            resident_id = request.form['resident_id']
            quantity = int(request.form['quantity'])
            date = datetime.now()

            print(f"DEBUG: Iniciando creación de entrega - Supply ID: {supply_id}, Cantidad: {quantity}")

            # Obtener el suministro y bloquearlo para actualización
            supply = Supply.query.get(supply_id)
            if not supply:
                return "Suministro no encontrado", 400

            print(f"DEBUG: Estado inicial del suministro - ID: {supply.id}, Nombre: {supply.name}, Cantidad actual: {supply.quantity}")

            # Actualizar cantidad del suministro directamente
            supply.quantity = supply.quantity - quantity
            if supply.quantity < 0:
                return f"No hay suficiente cantidad disponible. Stock actual: {supply.quantity + quantity}", 400

            print(f"DEBUG: Nueva cantidad calculada: {supply.quantity}")

            # Crear la entrega
            new_delivery = Delivery(
                supply_id=supply_id,
                resident_id=resident_id,
                quantity=quantity,
                date=date
            )
            
            print(f"DEBUG: Entrega creada en memoria - Cantidad: {new_delivery.quantity}")
            
            # Guardar los cambios
            db.session.add(new_delivery)
            db.session.add(supply)
            db.session.commit()
            
            print(f"DEBUG: Cambios guardados. Cantidad final en suministro: {supply.quantity}")
            
            return redirect(url_for('delivery_bp.list_deliveries'))
            
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Error al crear entrega: {str(e)}")
            return "Error al crear la entrega", 400

    supplies = Supply.query.all()
    residents = Resident.query.all()
    return render_template('create_delivery.html', supplies=supplies, residents=residents)

@delivery_bp.route('/admin/deliveries/edit/<int:id>', methods=['GET', 'POST'])
def edit_delivery(id):
    delivery = Delivery.query.get_or_404(id)
    if request.method == 'POST':
        # Guardar la cantidad anterior para restaurarla si algo falla
        old_quantity = delivery.quantity
        old_supply = delivery.supply
        
        # Actualizar datos de la entrega
        delivery.supply_id = request.form['supply_id']
        delivery.resident_id = request.form['resident_id']
        delivery.quantity = int(request.form['quantity'])
        delivery.date = datetime.now()

        # Restaurar la cantidad anterior del suministro
        if old_supply:
            old_supply.quantity += old_quantity
        
        # Intentar actualizar la nueva cantidad
        if delivery.update_supply_quantity():
            db.session.commit()
            return redirect(url_for('delivery_bp.list_deliveries'))
        else:
            # Si falla, restaurar todo al estado anterior
            delivery.quantity = old_quantity
            delivery.supply_id = old_supply.id if old_supply else None
            db.session.rollback()
            return "No hay suficiente cantidad disponible del suministro", 400

    supplies = Supply.query.all()
    residents = Resident.query.all()
    return render_template('edit_delivery.html', delivery=delivery, supplies=supplies, residents=residents)

@delivery_bp.route('/admin/deliveries/delete/<int:id>', methods=['POST'])
def delete_delivery(id):
    delivery = Delivery.query.get_or_404(id)
    
    # Restaurar la cantidad al suministro
    if delivery.supply:
        delivery.supply.quantity += delivery.quantity
    
    db.session.delete(delivery)
    db.session.commit()
    return redirect(url_for('delivery_bp.list_deliveries'))
