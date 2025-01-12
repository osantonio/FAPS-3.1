from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify, current_app
from ..models import Supply, StoreType, Delivery, Resident
from ..extensions import db
from ..routes.auth_routes import login_required
from datetime import datetime

store_bp = Blueprint('store_bp', __name__)

def init_store_types():
    # Verificar si ya existen tipos de tienda
    if StoreType.query.first() is None:
        # Crear tipos de tienda
        bodega = StoreType(
            name='bodega',
            can_distribute_to_beneficiaries=True,
            can_distribute_to_store=True,
            can_distribute_to_warehouse=True
        )
        
        almacen = StoreType(
            name='almacen',
            can_distribute_to_beneficiaries=True,
            can_distribute_to_store=True,
            can_distribute_to_warehouse=False
        )
        
        tienda = StoreType(
            name='tienda',
            can_distribute_to_beneficiaries=True,
            can_distribute_to_store=False,
            can_distribute_to_warehouse=False
        )
        
        db.session.add(bodega)
        db.session.add(almacen)
        db.session.add(tienda)
        db.session.commit()

# Variable para controlar si ya se inicializaron los tipos de tienda
_store_types_initialized = False

@store_bp.before_app_request
def setup_store_types():
    global _store_types_initialized
    if not _store_types_initialized:
        with current_app.app_context():
            init_store_types()
            _store_types_initialized = True

@store_bp.route('/store')
@login_required
def store():
    # Si es colaborador, solo mostrar productos de tienda
    if session.get('user_type') == 'colaborador':
        tienda = StoreType.query.filter_by(name='tienda').first()
        supplies = Supply.query.filter_by(store_type_id=tienda.id).all()
    else:
        supplies = Supply.query.all()
        
    if 'cart' not in session:
        session['cart'] = []
        session['cart_count'] = 0
    return render_template('store/store.html', supplies=supplies)

@store_bp.route('/cart')
@login_required
def view_cart():
    cart_items = []
    total_items = 0
    
    if 'cart' not in session:
        session['cart'] = []
    
    for item in session['cart']:
        supply = Supply.query.get(item.get('id'))
        if supply:
            cart_items.append({
                'id': supply.id,
                'name': supply.name,
                'photo': supply.photo,
                'quantity': item.get('quantity', 1),
                'stock': supply.quantity
            })
            total_items += item.get('quantity', 1)
    
    session['cart_count'] = total_items
    residents = Resident.query.all()
    return render_template('store/cart.html', cart_items=cart_items, residents=residents)

@store_bp.route('/finalize-cart', methods=['POST'])
@login_required
def finalize_cart():
    try:
        resident_id = request.form.get('resident_id')
        if not resident_id:
            return jsonify({
                'success': False,
                'message': 'Debes seleccionar un beneficiario'
            })

        if 'cart' not in session or not session['cart']:
            return jsonify({
                'success': False,
                'message': 'El carrito está vacío'
            })

        # Crear entregas para cada item en el carrito
        for item in session['cart']:
            supply = Supply.query.get(item.get('id'))
            if supply:
                quantity = item.get('quantity', 1)
                
                # Verificar stock
                if supply.quantity < quantity:
                    return jsonify({
                        'success': False,
                        'message': f'Stock insuficiente para {supply.name}'
                    })
                
                # Crear entrega
                delivery = Delivery(
                    supply_id=supply.id,
                    resident_id=resident_id,
                    quantity=quantity,
                    date=datetime.now()
                )
                
                # Actualizar stock
                supply.quantity -= quantity
                
                db.session.add(delivery)
        
        # Guardar cambios y limpiar carrito
        db.session.commit()
        session['cart'] = []
        session['cart_count'] = 0
        
        return jsonify({
            'success': True,
            'message': 'Entrega registrada exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al procesar la entrega: {str(e)}'
        })

@store_bp.route('/add-to-cart/<int:supply_id>', methods=['POST'])
@login_required
def add_to_cart(supply_id):
    try:
        if 'cart' not in session:
            session['cart'] = []
            
        supply = Supply.query.get_or_404(supply_id)
        
        if supply.quantity <= 0:
            return jsonify({
                'success': False,
                'message': 'Producto agotado'
            })

        # Buscar si el producto ya está en el carrito
        for item in session['cart']:
            if item.get('id') == supply_id:
                if item.get('quantity', 1) < supply.quantity:
                    item['quantity'] = item.get('quantity', 1) + 1
                    session.modified = True
                    return jsonify({
                        'success': True,
                        'message': 'Producto agregado al carrito',
                        'cart_count': sum(item.get('quantity', 1) for item in session['cart'])
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Stock no disponible'
                    })

        # Si no está en el carrito, agregarlo
        session['cart'].append({
            'id': supply_id,
            'quantity': 1
        })
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Producto agregado al carrito',
            'cart_count': sum(item.get('quantity', 1) for item in session['cart'])
        })
        
    except Exception as e:
        print(f"Error en add_to_cart: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al agregar al carrito'
        })

@store_bp.route('/remove-from-cart/<int:supply_id>', methods=['POST'])
@login_required
def remove_from_cart(supply_id):
    try:
        if 'cart' not in session:
            session['cart'] = []
            return jsonify({
                'success': True,
                'message': 'Carrito vacío',
                'cart_count': 0
            })
            
        session['cart'] = [item for item in session['cart'] if item.get('id') != supply_id]
        session.modified = True
        cart_count = sum(item.get('quantity', 1) for item in session['cart'])
        
        return jsonify({
            'success': True,
            'message': 'Producto eliminado del carrito',
            'cart_count': cart_count
        })
    except Exception as e:
        print(f"Error en remove_from_cart: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Error al eliminar del carrito'
        }) 