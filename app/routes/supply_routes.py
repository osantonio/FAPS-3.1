from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Supply

# Ruta para crear un nuevo suministro
@app.route('/admin/supplies/create', methods=['GET', 'POST'])
def create_supply():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        entry_date = request.form['entry_date']

        new_supply = Supply(
            name=name,
            category=category,
            quantity=quantity,
            entry_date=entry_date
        )
        db.session.add(new_supply)
        db.session.commit()
        return redirect(url_for('list_supplies'))
    return render_template('create_supply.html')

# Ruta para listar suministros
@app.route('/admin/supplies')
def list_supplies():
    supplies = Supply.query.all()
    return render_template('list_supplies.html', supplies=supplies)

# Ruta para editar un suministro
@app.route('/admin/supplies/edit/<int:id>', methods=['GET', 'POST'])
def edit_supply(id):
    supply = Supply.query.get_or_404(id)
    if request.method == 'POST':
        supply.name = request.form['name']
        supply.category = request.form['category']
        supply.quantity = request.form['quantity']
        supply.entry_date = request.form['entry_date']
        db.session.commit()
        return redirect(url_for('list_supplies'))
    return render_template('edit_supply.html', supply=supply)

# Ruta para eliminar un suministro
@app.route('/admin/supplies/delete/<int:id>', methods=['POST'])
def delete_supply(id):
    supply = Supply.query.get_or_404(id)
    db.session.delete(supply)
    db.session.commit()
    return redirect(url_for('list_supplies'))