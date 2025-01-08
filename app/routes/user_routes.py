from flask import render_template, request, redirect, url_for
from app import app
from app.extensions import db, bcrypt  # Importar las extensiones desde `extensions.py`
from app.models import User

# Ruta para crear un nuevo usuario
@app.route('/admin/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Recoger datos del formulario
        name = request.form['name']
        lastname = request.form['lastname']
        birthday_date = request.form['birthday_date']
        no_identification = request.form['no_identification']
        password = request.form['password']
        type_user = request.form['type_user']

        # Crear una nueva instancia de User
        new_user = User(
            name=name,
            lastname=lastname,
            birthday_date=birthday_date,
            no_identification=no_identification,
            type_user=type_user
        )
        # Establecer la contraseña utilizando `bcrypt`
        new_user.set_password(password)
        # Añadir el nuevo usuario a la sesión de la base de datos y hacer commit
        db.session.add(new_user)
        db.session.commit()
        # Redirigir a la lista de usuarios
        return redirect(url_for('list_users'))
    return render_template('create_user.html')

# Ruta para listar usuarios
@app.route('/admin/users')
def list_users():
    # Recuperar todos los usuarios de la base de datos
    users = User.query.all()
    return render_template('list_users.html', users=users)

# Ruta para editar un usuario existente
@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    # Recuperar el usuario por su ID
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        # Actualizar los datos del usuario con los datos del formulario
        user.name = request.form['name']
        user.lastname = request.form['lastname']
        user.birthday_date = request.form['birthday_date']
        user.no_identification = request.form['no_identification']
        user.type_user = request.form['type_user']
        if request.form['password']:
            user.set_password(request.form['password'])
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('edit_user.html', user=user)

# Ruta para eliminar un usuario existente
@app.route('/admin/users/delete/<int:id>', methods=['POST'])
def delete_user(id):
    # Recuperar el usuario por su ID
    user = User.query.get_or_404(id)
    # Eliminar el usuario de la sesión de la base de datos y hacer commit
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))
