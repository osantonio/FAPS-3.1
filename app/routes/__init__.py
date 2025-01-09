from .delivery_routes import delivery_bp
from .user_routes import user_bp
from .resident_routes import resident_bp
from .supply_routes import supply_bp

def register_blueprints(app):
    """Registra todos los blueprints de la aplicación"""
    app.register_blueprint(delivery_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(resident_bp)
    app.register_blueprint(supply_bp) 