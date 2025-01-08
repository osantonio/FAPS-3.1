from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import User

# Ruta para crear un nuevo usuario
@app.route('/admin/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        birthday_date = request.form['birthday_date']
        no_identification = request.form['no_identification']
        password = request.form['password']
        type_user = request.form['type_user']

        new_user = User(
            name=name,
            lastname=lastname,
            birthday_date=birthday_date,
            no_identification=no_identification,
            type_user=type_user
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('create_user.html')

# Ruta para listar usuarios
@app.route('/admin/users')
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)

# Ruta para editar un usuario
@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
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

# Ruta para eliminar un usuario
@app.route('/admin/users/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))
