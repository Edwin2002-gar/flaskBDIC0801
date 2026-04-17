from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Alumnos
import forms_alumnos

alumnos = Blueprint('alumnos', __name__)

@alumnos.route("/alumnos")
def lista_alumnos():
    alumnos_list = Alumnos.query.all()
    return render_template("alumnos/index_alumnos.html", alumnos=alumnos_list)

@alumnos.route("/alumnos/nuevo", methods=['GET', 'POST'])
def nuevo_alumno():
    form = forms_alumnos.AlumnoForm(request.form)
    
    if request.method == 'POST' and form.validate():
        
        alumno_existente = Alumnos.query.filter_by(email=form.email.data).first()
        
        if alumno_existente:
            # Si existe, mandamos el mensaje bonito y recargamos el formulario
            flash('⚠️ El email ya está registrado en el sistema', 'danger')
            return render_template("alumnos/nuevo.html", form=form)
            
        # 2. SI NO EXISTE, GUARDAMOS NORMALMENTE
        try:
            alumno = Alumnos(
                nombre=form.nombre.data,
                apaterno=form.apaterno.data,
                amaterno=form.amaterno.data,
                edad=form.edad.data,
                email=form.email.data
            )
            db.session.add(alumno)
            db.session.commit()
            flash('Alumno registrado exitosamente', 'success')
            return redirect(url_for('alumnos.lista_alumnos'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'danger')
            
    return render_template("alumnos/nuevo.html", form=form)

@alumnos.route("/alumnos/editar/<int:id>", methods=['GET', 'POST'])
def editar_alumno(id):
    alumno = Alumnos.query.get_or_404(id)
    form = forms_alumnos.AlumnoForm(request.form, obj=alumno)
    
    if request.method == 'POST' and form.validate():
        try:
            alumno.nombre = form.nombre.data
            alumno.apaterno = form.apaterno.data
            alumno.amaterno = form.amaterno.data
            alumno.edad = form.edad.data
            alumno.email = form.email.data
            db.session.commit()
            flash('Alumno actualizado exitosamente', 'success')
            return redirect(url_for('alumnos.lista_alumnos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    return render_template("alumnos/editar.html", form=form, alumno=alumno)

@alumnos.route("/alumnos/eliminar/<int:id>")
def eliminar_alumno(id):
    try:
        alumno = Alumnos.query.get_or_404(id)
        db.session.delete(alumno)
        db.session.commit()
        flash('Alumno eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    return redirect(url_for('alumnos.lista_alumnos'))