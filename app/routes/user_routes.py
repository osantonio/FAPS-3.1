from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import User
from datetime import datetime

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/admin/users')
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)

@user_bp.route('/admin/users/create', methods=['GET', 'POST'])
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
        return redirect(url_for('user_bp.list_users'))
    return render_template('create_user.html')

@user_bp.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('user_bp.list_users'))
    return render_template('edit_user.html', user=user)

@user_bp.route('/admin/users/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_bp.list_users'))
