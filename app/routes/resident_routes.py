from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import Resident
from datetime import datetime

resident_bp = Blueprint('resident_bp', __name__)

@resident_bp.route('/admin/residents')
def list_residents():
    residents = Resident.query.all()
    return render_template('list_residents.html', residents=residents)

@resident_bp.route('/admin/residents/create', methods=['GET', 'POST'])
def create_resident():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        birthday_date = request.form['birthday_date']
        no_identification = request.form['no_identification']
        health_status = request.form['health_status']
        medical_conditions = request.form['medical_conditions']
        medications = request.form['medications']
        medical_history = request.form['medical_history']
        special_requirements = request.form['special_requirements']

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
        
        db.session.add(new_resident)
        db.session.commit()
        return redirect(url_for('resident_bp.list_residents'))
    return render_template('create_resident.html')

@resident_bp.route('/admin/residents/edit/<int:id>', methods=['GET', 'POST'])
def edit_resident(id):
    resident = Resident.query.get_or_404(id)
    if request.method == 'POST':
        resident.name = request.form['name']
        resident.lastname = request.form['lastname']
        resident.birthday_date = request.form['birthday_date']
        resident.no_identification = request.form['no_identification']
        resident.health_status = request.form['health_status']
        resident.medical_conditions = request.form['medical_conditions']
        resident.medications = request.form['medications']
        resident.medical_history = request.form['medical_history']
        resident.special_requirements = request.form['special_requirements']
        db.session.commit()
        return redirect(url_for('resident_bp.list_residents'))
    return render_template('edit_resident.html', resident=resident)

@resident_bp.route('/admin/residents/delete/<int:id>', methods=['POST'])
def delete_resident(id):
    resident = Resident.query.get_or_404(id)
    db.session.delete(resident)
    db.session.commit()
    return redirect(url_for('resident_bp.list_residents'))