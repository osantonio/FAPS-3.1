from flask import Flask
from flask_caching import Cache
from flask_talisman import Talisman
from flask_migrate import Migrate
from .extensions import db, bcrypt
from .models import User
from .routes import register_blueprints

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

# Registrar Blueprints
register_blueprints(app)

# Importar rutas después de crear la aplicación
from . import routes
import main  # Importar main.py que contiene la ruta del dashboard

# Crear todas las tablas en la base de datos
with app.app_context():
    db.create_all()