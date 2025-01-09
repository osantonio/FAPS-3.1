from flask import Blueprint, render_template, request, redirect, url_for
from .extensions import db
from .models import User, Resident, Supply, Delivery
from datetime import datetime

# Definir Blueprints
user_bp = Blueprint('user_bp', __name__)
resident_bp = Blueprint('resident_bp', __name__)
supply_bp = Blueprint('supply_bp', __name__)
delivery_bp = Blueprint('delivery_bp', __name__)

# Rutas para el manejo de usuarios
@user_bp.route('/admin/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
        no_identification = request.form['no_identification']
        password = request.form['password']
        type_user = request.form['type_user']

        new_user = User(
            name=name,
            lastname=lastname,
            birthday_date=birthday_date,
            no_identification=no_identification,
            type_user=type_user
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_bp.list_users'))
    return render_template('create_user.html')

@user_bp.route('/admin/users')
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)

@user_bp.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.lastname = request.form['lastname']
        user.birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
        user.no_identification = request.form['no_identification']
        user.type_user = request.form['type_user']
        if request.form['password']:
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

# Rutas para el manejo de residentes
@resident_bp.route('/admin/residents/create', methods=['GET', 'POST'])
def create_resident():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
        no_identification = request.form['no_identification']
        health_status = request.form['health_status']
        medical_conditions = request.form['medical_conditions']
        medications = request.form['medications']
        medical_history = request.form['medical_history']
        special_requirements = request.form['special_requirements']

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
        db.session.add(new_resident)
        db.session.commit()
        return redirect(url_for('resident_bp.list_residents'))
    return render_template('create_resident.html')

@resident_bp.route('/admin/residents')
def list_residents():
    residents = Resident.query.all()
    return render_template('list_residents.html', residents=residents)

@resident_bp.route('/admin/residents/edit/<int:id>', methods=['GET', 'POST'])
def edit_resident(id):
    resident = Resident.query.get_or_404(id)
    if request.method == 'POST':
        resident.name = request.form['name']
        resident.lastname = request.form['lastname']
        resident.birthday_date = datetime.strptime(request.form['birthday_date'], '%Y-%m-%d')
        resident.no_identification = request.form['no_identification']
        resident.health_status = request.form['health_status']
        resident.medical_conditions = request.form['medical_conditions']
        resident.medications = request.form['medications']
        resident.medical_history = request.form['medical_history']
        resident.special_requirements = request.form['special_requirements']
        db.session.commit()
        return redirect(url_for('resident_bp.list_residents'))
    return render_template('edit_resident.html', resident=resident)

@resident_bp.route('/admin/residents/delete/<int:id>', methods=['POST'])
def delete_resident(id):
    resident = Resident.query.get_or_404(id)
    db.session.delete(resident)
    db.session.commit()
    return redirect(url_for('resident_bp.list_residents'))

# Rutas para el manejo de suministros
@supply_bp.route('/admin/supplies/create', methods=['GET', 'POST'])
def create_supply():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        entry_date = datetime.now()

        new_supply = Supply(
            name=name,
            category=category,
            quantity=quantity,
            entry_date=entry_date
        )
        db.session.add(new_supply)
        db.session.commit()
        return redirect(url_for('supply_bp.list_supplies'))
    return render_template('create_supply.html')

@supply_bp.route('/admin/supplies')
def list_supplies():
    supplies = Supply.query.all()
    return render_template('list_supplies.html', supplies=supplies)

@supply_bp.route('/admin/supplies/edit/<int:id>', methods=['GET', 'POST'])
def edit_supply(id):
    supply = Supply.query.get_or_404(id)
    if request.method == 'POST':
        supply.name = request.form['name']
        supply.category = request.form['category']
        supply.quantity = request.form['quantity']
        supply.entry_date = datetime.now()
        db.session.commit()
        return redirect(url_for('supply_bp.list_supplies'))
    return render_template('edit_supply.html', supply=supply)

@supply_bp.route('/admin/supplies/delete/<int:id>', methods=['POST'])
def delete_supply(id):
    supply = Supply.query.get_or_404(id)
    db.session.delete(supply)
    db.session.commit()
    return redirect(url_for('supply_bp.list_supplies'))

# Rutas para el manejo de entregas
@delivery_bp.route('/admin/deliveries/create', methods=['GET', 'POST'])
def create_delivery():
    if request.method == 'POST':
        supply_id = request.form['supply_id']
        resident_id = request.form['resident_id']
        quantity = request.form['quantity']
        date = datetime.now()

        new_delivery = Delivery(
            supply_id=supply_id,
            resident_id=resident_id,
            quantity=quantity,
            date=date
        )
        db.session.add(new_delivery)
        db.session.commit()
        return redirect(url_for('delivery_bp.list_deliveries'))
    supplies = Supply.query.all()
    residents = Resident.query.all()
    return render_template('create_delivery.html', supplies=supplies, residents=residents)

@delivery_bp.route('/admin/deliveries')
def list_deliveries():
    deliveries = Delivery.query.all()
    return render_template('list_deliveries.html', deliveries=deliveries)

@delivery_bp.route('/admin/deliveries/edit/<int:id>', methods=['GET', 'POST'])
def edit_delivery(id):
    delivery = Delivery.query.get_or_404(id)
    if request.method == 'POST':
        delivery.supply_id = request.form['supply_id']
        delivery.resident_id = request.form['resident_id']
        delivery.quantity = request.form['quantity']
        delivery.date = request.form['date']
        db.session.commit()
        return redirect(url_for('delivery_bp.list_deliveries'))
    supplies = Supply.query.all()
    residents = Resident.query.all()
    return render_template('edit_delivery.html', delivery=delivery, supplies=supplies, residents=residents)

@delivery_bp.route('/admin/deliveries/delete/<int:id>', methods=['POST'])
def delete_delivery(id):
    delivery = Delivery.query.get_or_404(id)
    db.session.delete(delivery)
    db.session.commit()
    return redirect(url_for('delivery_bp.list_deliveries'))

# Registrar Blueprints
def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(resident_bp)
    app.register_blueprint(supply_bp)
    app.register_blueprint(delivery_bp)
