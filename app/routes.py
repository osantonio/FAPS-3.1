from . import db, bcrypt, roles_users
from flask_security import UserMixin, RoleMixin


# Modelo de roles
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# Modelo unificado de usuarios
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime)
    nombre = db.Column(db.String(100), nullable=False)  # Nombre completo
    no_identificacion = db.Column(db.String(100), unique=True, nullable=True)  # ID único o cédula
    tipo_usuario = db.Column(db.String(50), nullable=False, default="colaborador")  # "admin" o "colaborador"
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

# Modelo de beneficiarios
class Beneficiario(db.Model):
    id_beneficiario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    salud_estado = db.Column(db.String(255), nullable=True)
    salud_condiciones_medicas = db.Column(db.Text, nullable=True)
    salud_alergias = db.Column(db.Text, nullable=True)
    salud_medicamentos = db.Column(db.Text, nullable=True)
    salud_historial_medico = db.Column(db.Text, nullable=True)
    salud_requerimientos_especiales = db.Column(db.Text, nullable=True)
    habitacion = db.Column(db.String(50), nullable=True)

# Modelo de suministros
class Suministro(db.Model):
    id_suministro = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_entrada = db.Column(db.Date, nullable=False)

# Modelo de entregas
class Entrega(db.Model):
    id_entrega = db.Column(db.Integer, primary_key=True)
    id_suministro = db.Column(db.Integer, db.ForeignKey('suministro.id'))
    id_beneficiario = db.Column(db.Integer, db.ForeignKey('beneficiario.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)