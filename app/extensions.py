# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Instancias de extensiones Flask
db = SQLAlchemy()
bcrypt = Bcrypt()
