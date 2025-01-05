from flask import render_template, request, redirect, url_for
from . import app, db
from .models import Suministro, Beneficiario, Entrega

@app.route('/inventario', methods=['GET', 'POST'])
def gestionar_inventario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        fecha_entrada = request.form['fecha_entrada']
        nuevo_suministro = Suministro(nombre=nombre, categoria=categoria, cantidad=cantidad, fecha_entrada=fecha_entrada)
        db.session.add(nuevo_suministro)
        db.session.commit()
        return redirect(url_for('gestionar_inventario'))
    suministros = Suministro.query.all()
    return render_template('inventario.html', suministros=suministros)

@app.route('/entregas', methods=['GET', 'POST'])
def gestionar_entregas():
    if request.method == 'POST':
        id_suministro = request.form['id_suministro']
        id_beneficiario = request.form['id_beneficiario']
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        nueva_entrega = Entrega(id_suministro=id_suministro, id_beneficiario=id_beneficiario, cantidad=cantidad, fecha=fecha)
        db.session.add(nueva_entrega)
        db.session.commit()
        return redirect(url_for('gestionar_entregas'))
    entregas = Entrega.query.all()
    return render_template('entregas.html', entregas=entregas)
