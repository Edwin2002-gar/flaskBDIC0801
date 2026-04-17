from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Maestros
import forms_maestros

# Creamos el Blueprint para los maestros
maestros = Blueprint('maestros', __name__)

@maestros.route("/maestros")
def lista_maestros():
    maestros_db = Maestros.query.all()
    return render_template("maestros/maestros_lista.html", maestros=maestros_db)

@maestros.route("/maestros/nuevo", methods=['GET', 'POST'])
def nuevo_maestro():
    form = forms_maestros.MaestroForm(request.form)
    
    if request.method == 'POST' and form.validate():
        # Validar que el email no exista duplicado
        maestro_existente = Maestros.query.filter_by(email=form.email.data).first()
        if maestro_existente:
            flash('⚠️ El email ya está registrado para otro maestro', 'danger')
            return render_template("maestros/maestro_form.html", form=form)

        try:
            maestro = Maestros(
                nombre=form.nombre.data,
                apellidos=form.apellidos.data,
                email=form.email.data,
                especialidad=form.especialidad.data
            )
            db.session.add(maestro)
            db.session.commit()
            flash('Maestro registrado exitosamente', 'success')
            return redirect(url_for('maestros.lista_maestros'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'danger')
            
    return render_template("maestros/maestro_form.html", form=form)

@maestros.route("/maestros/editar/<int:matricula>", methods=['GET', 'POST'])
def editar_maestro(matricula):
    maestro = Maestros.query.get_or_404(matricula)
    form = forms_maestros.MaestroForm(request.form, obj=maestro)
    
    if request.method == 'POST' and form.validate():
        try:
            maestro.nombre = form.nombre.data
            maestro.apellidos = form.apellidos.data
            maestro.email = form.email.data
            maestro.especialidad = form.especialidad.data
            db.session.commit()
            flash('Maestro actualizado exitosamente', 'success')
            return redirect(url_for('maestros.lista_maestros'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    return render_template("maestros/maestro_form.html", form=form, maestro=maestro)

@maestros.route("/maestros/eliminar/<int:matricula>")
def eliminar_maestro(matricula):
    try:
        maestro = Maestros.query.get_or_404(matricula)
        db.session.delete(maestro)
        db.session.commit()
        flash('Maestro eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    return redirect(url_for('maestros.lista_maestros'))