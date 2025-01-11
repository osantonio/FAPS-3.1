from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.extensions import db
from app.models import Supply, CartItem, User, Delivery, Resident
from datetime import datetime
import os

store_bp = Blueprint('store_bp', __name__)

def update_cart_count():
    """Actualiza el contador del carrito en la sesión"""
    user_id = session.get('user_id')
    if user_id:
        count = CartItem.query.filter_by(user_id=user_id).count()
        session['cart_count'] = count

@store_bp.route('/store')
def store():
    if not session.get('user_id'):
        return redirect(url_for('auth_bp.login'))
    supplies = Supply.query.all()
    return render_template('store/store.html', supplies=supplies)

@store_bp.route('/cart')
def view_cart():
    if not session.get('user_id'):
        return redirect(url_for('auth_bp.login'))
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    residents = Resident.query.all()
    return render_template('store/cart.html', cart_items=cart_items, residents=residents)

@store_bp.route('/cart/add/<int:supply_id>', methods=['POST'])
def add_to_cart(supply_id):
    if not session.get('user_id'):
        flash('No autorizado', 'danger')
        return redirect(url_for('auth_bp.login'))
        
    try:
        quantity = int(request.get_json().get('quantity', 1))
        
        # Validaciones
        if quantity <= 0:
            flash('La cantidad debe ser mayor que 0', 'warning')
            return jsonify({'redirect': url_for('store_bp.store')})
            
        supply = Supply.query.get_or_404(supply_id)
        if supply.quantity < quantity:
            flash('No hay suficiente stock disponible', 'warning')
            return jsonify({'redirect': url_for('store_bp.store')})
            
        # Verificar si ya existe en el carrito
        cart_item = CartItem.query.filter_by(
            user_id=session['user_id'],
            supply_id=supply_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=session['user_id'],
                supply_id=supply_id,
                quantity=quantity
            )
            db.session.add(cart_item)
            
        db.session.commit()
        update_cart_count()
        flash(f'Se añadió {quantity} unidad(es) de {supply.name} al carrito', 'success')
        return jsonify({'redirect': url_for('store_bp.store')})
        
    except Exception as e:
        db.session.rollback()
        flash('Error al añadir al carrito', 'danger')
        return jsonify({'redirect': url_for('store_bp.store')})

@store_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if not session.get('user_id'):
        flash('No autorizado', 'danger')
        return redirect(url_for('auth_bp.login'))
        
    try:
        cart_item = CartItem.query.get_or_404(item_id)
        if cart_item.user_id != session['user_id']:
            flash('No autorizado', 'danger')
            return redirect(url_for('store_bp.cart'))
            
        supply_name = cart_item.supply.name
        db.session.delete(cart_item)
        db.session.commit()
        update_cart_count()
        flash(f'Se eliminó {supply_name} del carrito', 'success')
        return redirect(url_for('store_bp.cart'))
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar del carrito', 'danger')
        return redirect(url_for('store_bp.cart'))

@store_bp.route('/cart/checkout', methods=['POST'])
def checkout():
    if not session.get('user_id'):
        flash('No autorizado', 'danger')
        return redirect(url_for('auth_bp.login'))
        
    try:
        data = request.get_json()
        resident_id = data.get('resident_id')
        if not resident_id:
            flash('Debe seleccionar un beneficiario', 'warning')
            return jsonify({'redirect': url_for('store_bp.cart')})
            
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        if not cart_items:
            flash('El carrito está vacío', 'warning')
            return jsonify({'redirect': url_for('store_bp.cart')})
            
        # Crear entregas para cada item
        for item in cart_items:
            # Verificar stock nuevamente
            if item.supply.quantity < item.quantity:
                flash(f'No hay suficiente stock de {item.supply.name}', 'warning')
                return jsonify({'redirect': url_for('store_bp.cart')})
                
            # Crear la entrega
            delivery = Delivery(
                supply_id=item.supply_id,
                resident_id=resident_id,
                quantity=item.quantity,
                date=datetime.now()
            )
            
            # Actualizar stock
            item.supply.quantity -= item.quantity
            
            # Añadir entrega
            db.session.add(delivery)
            # Eliminar item del carrito
            db.session.delete(item)
            
        db.session.commit()
        update_cart_count()
        flash('Entrega realizada con éxito', 'success')
        return jsonify({'redirect': url_for('delivery_bp.list_deliveries')})
        
    except Exception as e:
        db.session.rollback()
        flash('Error al procesar la entrega', 'danger')
        return jsonify({'redirect': url_for('store_bp.cart')}) 