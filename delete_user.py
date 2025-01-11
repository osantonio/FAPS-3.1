from app import app, db
from app.models import User

with app.app_context():
    user = User.query.filter_by(name='CAMILA').first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print(f"Usuario {user.name} eliminado exitosamente")
    else:
        print("Usuario no encontrado") 