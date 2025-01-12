from flask import Blueprint, render_template
from datetime import datetime
from ..models import User, Resident, Supply, Delivery
from ..routes.auth_routes import login_required

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    # Contadores de entidades
    users_count = User.query.count()
    residents_count = Resident.query.count()
    supplies_count = Supply.query.count()
    deliveries_count = Delivery.query.count()

    # Fecha actual
    current_date = datetime.now().strftime('%d/%m/%Y')

    # Actividades recientes (ejemplo)
    activities = [
        {
            'type': 'Creación',
            'type_class': 'primary',
            'description': 'Nuevo residente agregado',
            'user': 'Admin',
            'date': current_date
        },
        {
            'type': 'Actualización', 
            'type_class': 'warning',
            'description': 'Suministro modificado',
            'user': 'Admin', 
            'date': current_date
        }
    ]

    # Definir stats
    stats = {
        'users_count': users_count,
        'residents_count': residents_count,
        'supplies_count': supplies_count,
        'deliveries_count': deliveries_count
    }

    return render_template(
        'dashboard.html', 
        current_date=current_date,
        activities=activities,
        stats=stats
    ) 