from .extensions import db, bcrypt

# Modelo unificado de usuarios
class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = (
        db.UniqueConstraint('no_identification', name='uq_user_identification'),
    )

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    birthday_date = db.Column(db.Date, nullable=False)
    no_identification = db.Column(db.Integer, nullable=False)
    type_user = db.Column(db.String(50), nullable=False, default="colaborador")
    profile_photo = db.Column(db.String(255), nullable=True)

    def is_active(self):
        return self.active

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
    photo = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)  # Para mostrar el valor referencial

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

# Modelo para items del carrito
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Relaciones
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    supply = db.relationship('Supply', backref=db.backref('cart_items', lazy=True))
