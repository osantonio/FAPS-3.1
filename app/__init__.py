from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_caching import Cache
from flask_security import Security, SQLAlchemyUserDatastore
from flask_talisman import Talisman

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
cache = Cache(app)
talisman = Talisman(app)

from .models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from .routes import *
