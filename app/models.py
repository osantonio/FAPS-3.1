from .extensions import db, bcrypt
from flask_security import UserMixin, RoleMixin
import uuid

# Tabla intermedia para la relación muchos a muchos entre usuarios y roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

delivery_supplies = db.Table('delivery_supplies',
    db.Column('delivery_id', db.Integer, db.ForeignKey('delivery.id'), primary_key=True),
    db.Column('supply_id', db.Integer, db.ForeignKey('supply.id'), primary_key=True)
)

# Modelo de roles
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# Modelo unificado de usuarios
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime)
    birthday_date = db.Column(db.Date, nullable=False)
    no_identification = db.Column(db.Integer, unique=True, nullable=False)
    type_user = db.Column(db.String(50), nullable=False, default="colaborador")
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

    def decrease_quantity(self, amount):
        """Disminuye la cantidad del suministro"""
        print(f"DEBUG Supply.decrease_quantity - ID: {self.id}, Cantidad actual: {self.quantity}, A descontar: {amount}")
        if self.quantity >= amount:
            old_quantity = self.quantity
            # Actualizar directamente en la base de datos
            result = db.session.execute(
                db.update(Supply).
                where(Supply.id == self.id).
                values(quantity=Supply.quantity - amount)
            )
            db.session.flush()
            # Recargar el objeto desde la base de datos
            db.session.refresh(self)
            print(f"DEBUG Supply.decrease_quantity - Cantidad actualizada de {old_quantity} a {self.quantity}")
            return True
        print(f"DEBUG Supply.decrease_quantity - Cantidad insuficiente. Necesita: {amount}, Disponible: {self.quantity}")
        return False

    def increase_quantity(self, amount):
        """Aumenta la cantidad del suministro"""
        old_quantity = self.quantity
        # Actualizar directamente en la base de datos
        result = db.session.execute(
            db.update(Supply).
            where(Supply.id == self.id).
            values(quantity=Supply.quantity + amount)
        )
        db.session.flush()
        # Recargar el objeto desde la base de datos
        db.session.refresh(self)
        print(f"DEBUG Supply.increase_quantity - Cantidad actualizada de {old_quantity} a {self.quantity}")
        return True

# Modelo de entregas
class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # Relaciones
    supply = db.relationship('Supply', backref=db.backref('deliveries', lazy=True))
    resident = db.relationship('Resident', backref=db.backref('deliveries', lazy=True))

    def update_supply_quantity(self):
        """Actualiza la cantidad del suministro después de una entrega"""
        try:
            supply = Supply.query.get(self.supply_id)
            if supply and self.quantity:
                if supply.quantity >= self.quantity:
                    supply.quantity -= self.quantity
                    db.session.add(supply)  # Aseguramos que el cambio se registre
                    db.session.flush()  # Forzamos la actualización
                    return True
                return False
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar cantidad: {str(e)}")
            return False











