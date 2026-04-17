from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Cursos, Maestros
import forms_cursos

# Creamos el Blueprint para los cursos
cursos = Blueprint('cursos', __name__)

@cursos.route("/cursos")
def lista_cursos():
    cursos_db = Cursos.query.all()
    return render_template("cursos/lista_cursos.html", cursos=cursos_db)

@cursos.route("/cursos/nuevo", methods=['GET', 'POST'])
def nuevo_curso():
    form = forms_cursos.CursoForm(request.form)
    
    # Llenamos el menú desplegable (dropdown) con los maestros de la base de datos
    form.maestro_id.choices = [(0, 'Seleccione un maestro')] + [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()
    ]
    
    if request.method == 'POST' and form.validate():
        # Validación extra: Evitar que se registren cursos con el mismo nombre
        curso_existente = Cursos.query.filter_by(nombre_curso=form.nombre_curso.data).first()
        if curso_existente:
            flash('⚠️ Este curso ya está registrado en el sistema', 'danger')
            return render_template("cursos/curso_form.html", form=form)

        try:
            nuevo_c = Cursos(
                nombre_curso=form.nombre_curso.data,
                maestro_id=form.maestro_id.data
            )
            db.session.add(nuevo_c)
            db.session.commit()
            flash('Curso creado exitosamente', 'success')
            return redirect(url_for('cursos.lista_cursos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el curso: {str(e)}', 'danger')
            
    return render_template("cursos/curso_form.html", form=form)

@cursos.route("/cursos/editar/<int:id>", methods=['GET', 'POST'])
def editar_curso(id):
    curso = Cursos.query.get_or_404(id)
    form = forms_cursos.CursoForm(request.form, obj=curso)
    
    # Volvemos a llenar el menú desplegable para la vista de edición
    form.maestro_id.choices = [(0, 'Seleccione un maestro')] + [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()
    ]
    
    if request.method == 'POST' and form.validate():
        try:
            curso.nombre_curso = form.nombre_curso.data
            curso.maestro_id = form.maestro_id.data
            db.session.commit()
            flash('Curso actualizado correctamente', 'success')
            return redirect(url_for('cursos.lista_cursos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')
            
    return render_template("cursos/curso_form.html", form=form, curso=curso)

@cursos.route("/cursos/eliminar/<int:id>")
def eliminar_curso(id):
    try:
        curso = Cursos.query.get_or_404(id)
        db.session.delete(curso)
        db.session.commit()
        flash('Curso eliminado del sistema', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    return redirect(url_for('cursos.lista_cursos'))