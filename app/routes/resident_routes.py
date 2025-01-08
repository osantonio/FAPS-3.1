from flask import render_template, request, redirect, url_for
from app import app
from app.extensions import db
from app.models import Resident

# Ruta para crear un nuevo residente
@app.route('/admin/residents/create', methods=['GET', 'POST'])
def create_resident():
    if request.method == 'POST':
        # Recoger datos del formulario
        name = request.form['name']
        lastname = request.form['lastname']
        birthday_date = request.form['birthday_date']
        no_identification = request.form['no_identification']
        health_status = request.form['health_status']
        medical_conditions = request.form['medical_conditions']
        medications = request.form['medications']
        medical_history = request.form['medical_history']
        special_requirements = request.form['special_requirements']

        # Crear una nueva instancia de Resident
        new_resident = Resident(
            name=name,
            lastname=lastname,
            birthday_date=birthday_date,
            no_identification=no_identification,
            health_status=health_status,
            medical_conditions=medical_conditions,
            medications=medications,
            medical_history=medical_history,
            special_requirements=special_requirements
        )
        # Añadir el nuevo residente a la sesión de la base de datos y hacer commit
        db.session.add(new_resident)
        db.session.commit