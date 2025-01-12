from app import app, db
from app.models import User
from datetime import datetime

def init_database():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("Base de datos inicializada correctamente")

        # Crear usuario administrador si no existe
        if not User.query.filter_by(no_identification='12345').first():
            admin_user = User(
                name='Admin',
                lastname='Sistema',
                birthday_date=datetime.now(),
                no_identification='12345',
                type_user='admin'
            )
            admin_user.set_password('12345')
            db.session.add(admin_user)
            db.session.commit()
            print("Usuario administrador creado exitosamente")
        else:
            print("El usuario administrador ya existe")

if __name__ == '__main__':
    init_database() 