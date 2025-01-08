from flask import Flask
from flask_login import LoginManager
from flask_caching import Cache
from flask_security import Security, SQLAlchemyUserDatastore
from flask_talisman import Talisman
from flask_migrate import Migrate # Importar Flask-Migrate
from .extensions import db, bcrypt
from .models import User, Role
from .routes import register_blueprints

app = Flask(__name__)
app.config.from_object('config')
app.config['DEBUG'] = True # Habilitar el modo de depuración

# Inicializar extensiones Flask
db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager(app)
cache = Cache(app)
talisman = Talisman(app)

# Inicializar Flask-Migrate
migrate = Migrate(app, db) #configurar Flask-Migrate

# Configurar Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Registrar Blueprints
register_blueprints(app)

# Crear todas las tablas en la base de datos
with app.app_context():
    db.create_all()