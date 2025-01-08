from . import db, bcrypt
from flask_security import UserMixin, RoleMixin
import uuid

# Tabla intermedia para la relación muchos a muchos entre usuarios y roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

# Modelo de roles
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# Modelo unificado de usuarios
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime)
    birthday_date = db.Column(db.Date, nullable=False)
    no_identification = db.Column(db.Integer, unique=True, nullable=False)
    type_user = db.Column(db.String(50), nullable=False, default="colaborador")
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    # Métodos para gestionar contraseñas
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# Modelo de residentes
class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    birthday_date = db.Column(db.Date, nullable=False)
    no_identification = db.Column(db.Integer, unique=True, nullable=False)
    health_status = db.Column(db.String(255), nullable=True)
    medical_conditions = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    medical_history = db.Column(db.Text, nullable=True)
    special_requirements = db.Column(db.Text, nullable=True)

# Modelo de suministros
class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.Date, nullable=False)

# Modelo de entregas
class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'))
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'))
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
