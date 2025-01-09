from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import Delivery, Supply, Resident
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

            # Obtener el suministro
            supply = Supply.query.get(supply_id)
            if not supply:
                return "Suministro no encontrado", 400

            # Verificar cantidad disponible
            if supply.quantity < quantity:
                return f"No hay suficiente cantidad disponible. Stock actual: {supply.quantity}", 400

            # Actualizar cantidad del suministro
            supply.quantity = supply.quantity - quantity

            # Crear la entrega
            new_delivery = Delivery(
                supply_id=supply_id,
                resident_id=resident_id,
                quantity=quantity,
                date=date
            )
            
            # Guardar los cambios
            db.session.add(new_delivery)
            db.session.add(supply)
            db.session.commit()
            
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
        try:
            # Guardar la cantidad anterior para restaurarla si algo falla
            old_quantity = delivery.quantity
            old_supply = delivery.supply
            
            # Actualizar datos de la entrega
            new_supply_id = request.form['supply_id']
            new_quantity = int(request.form['quantity'])

            # Si cambió el suministro o la cantidad
            if new_supply_id != str(delivery.supply_id) or new_quantity != delivery.quantity:
                # Restaurar cantidad al suministro anterior
                if old_supply:
                    old_supply.quantity += old_quantity
                
                # Verificar nuevo suministro
                new_supply = Supply.query.get(new_supply_id)
                if not new_supply:
                    return "Suministro no encontrado", 400
                
                # Verificar cantidad disponible
                if new_supply.quantity < new_quantity:
                    return f"No hay suficiente cantidad disponible. Stock actual: {new_supply.quantity}", 400
                
                # Actualizar cantidad del nuevo suministro
                new_supply.quantity -= new_quantity
                db.session.add(new_supply)

            # Actualizar la entrega
            delivery.supply_id = new_supply_id
            delivery.resident_id = request.form['resident_id']
            delivery.quantity = new_quantity
            delivery.date = datetime.now()
            
            db.session.commit()
            return redirect(url_for('delivery_bp.list_deliveries'))
            
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Error al editar entrega: {str(e)}")
            return "Error al editar la entrega", 400

    supplies = Supply.query.all()
    residents = Resident.query.all()
    return render_template('edit_delivery.html', delivery=delivery, supplies=supplies, residents=residents)

@delivery_bp.route('/admin/deliveries/delete/<int:id>', methods=['POST'])
def delete_delivery(id):
    try:
        delivery = Delivery.query.get_or_404(id)
        
        # Restaurar la cantidad al suministro
        if delivery.supply:
            delivery.supply.quantity += delivery.quantity
            db.session.add(delivery.supply)
        
        db.session.delete(delivery)
        db.session.commit()
        return redirect(url_for('delivery_bp.list_deliveries'))
    except Exception as e:
        db.session.rollback()
        print(f"ERROR: Error al eliminar entrega: {str(e)}")
        return "Error al eliminar la entrega", 400
