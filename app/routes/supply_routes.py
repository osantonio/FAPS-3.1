from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import Supply
from datetime import datetime
from app.routes.auth_routes import login_required, admin_required

supply_bp = Blueprint('supply_bp', __name__)

@supply_bp.route('/admin/supplies')
@login_required
def list_supplies():
    supplies = Supply.query.all()
    return render_template('list_supplies.html', supplies=supplies)

@supply_bp.route('/admin/supplies/create', methods=['GET', 'POST'])
@login_required
@admin_required
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

@supply_bp.route('/admin/supplies/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_supply(id):
    supply = Supply.query.get_or_404(id)
    if request.method == 'POST':
        supply.name = request.form['name']
        supply.category = request.form['category']
        supply.quantity = request.form['quantity']
        supply.entry_date = request.form['entry_date']
        db.session.commit()
        return redirect(url_for('supply_bp.list_supplies'))
    return render_template('edit_supply.html', supply=supply)

@supply_bp.route('/admin/supplies/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_supply(id):
    supply = Supply.query.get_or_404(id)
    db.session.delete(supply)
    db.session.commit()
    return redirect(url_for('supply_bp.list_supplies'))