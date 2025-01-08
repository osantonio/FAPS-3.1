from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Delivery, Supply, Resident

# Ruta para crear una nueva entrega
@app.route('/admin/deliveries/create', methods=['GET', 'POST'])
def create_delivery():
    if request.method == 'POST':
        supply_id = request.form['supply_id']
        resident_id = request.form['resident_id']
        quantity = request.form['quantity']
        date = request.form['date']

        new_delivery = Delivery(
            supply_id=supply_id,
            resident_id=resident_id,
            quantity=quantity,
            date=date
        )
        db.session.add(new_delivery)
        db.session.commit()
        return redirect(url_for('list_deliveries'))
    
    supplies = Supply.query.all()
    residents = Resident.query.all()
    return render_template('create_delivery.html', supplies=supplies, residents=residents)

# Ruta para listar entregas
@app.route('/admin/deliveries')
def list_deliveries():
    deliveries = Delivery.query.all()
    return render_template('list_deliveries.html', deliveries=deliveries)

# Ruta para editar una entrega
@app.route('/admin/deliveries/edit/<int:id>', methods=['GET', 'POST'])
def edit_delivery(id):
    delivery = Delivery.query.get_or_404(id)
    if request.method == 'POST':
        delivery.supply_id = request.form['supply_id']
        delivery.resident_id = request.form['resident_id']
        delivery.quantity = request.form['quantity']
        delivery.date = request.form['date']
        db.session.commit()
        return redirect(url_for('list_deliveries'))
    
    supplies = Supply.query.all()
    residents = Resident.query.all()
    return render_template('edit_delivery.html', delivery=delivery, supplies=supplies, residents=residents)

# Ruta para eliminar una entrega
@app.route('/admin/deliveries/delete/<int:id>', methods=['POST'])
def delete_delivery(id):
    delivery = Delivery.query.get_or_404(id)
    db.session.delete(delivery)
    db.session.commit()
    return redirect(url_for('list_deliveries'))