from app import app
from app.models import User
from app.extensions import db
from datetime import datetime

def create_test_user():
    with app.app_context():
        # Verificar si el usuario ya existe
        test_user = User.query.filter_by(no_identification=12345).first()
        if test_user is None:
            # Crear usuario de prueba
            user = User(
                name='Admin',
                lastname='Test',
                birthday_date=datetime.now(),
                no_identification=12345,
                type_user='admin'
            )
            user.set_password('12345')
            db.session.add(user)
            db.session.commit()
            print("Usuario de prueba creado exitosamente")
        else:
            print("El usuario de prueba ya existe")

if __name__ == '__main__':
    create_test_user() 