from flask import Flask
from flask_caching import Cache
from flask_talisman import Talisman
from flask_migrate import Migrate
from .extensions import db, bcrypt
from .models import User

app = Flask(__name__)
app.config.from_object('config')
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Recarga automática de templates
app.jinja_env.auto_reload = True  # Recarga automática de Jinja2

# Inicializar extensiones Flask
db.init_app(app)
bcrypt.init_app(app)
cache = Cache(app)

# Configurar Talisman para desarrollo local
talisman = Talisman(
    app,
    force_https=False,  # Deshabilitar forzado de HTTPS en desarrollo
    content_security_policy=None  # Deshabilitar CSP en desarrollo
)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Importar y registrar blueprints
from .routes.auth_routes import auth_bp
from .routes.main_routes import main_bp
from .routes.store_routes import store_bp
from .routes import user_bp, resident_bp, supply_bp, delivery_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(store_bp)
app.register_blueprint(user_bp)
app.register_blueprint(resident_bp)
app.register_blueprint(supply_bp)
app.register_blueprint(delivery_bp)

# Crear todas las tablas en la base de datos
with app.app_context():
    db.create_all()