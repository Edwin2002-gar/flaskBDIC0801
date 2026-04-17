from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig

from models import db, Alumnos, Maestros, Cursos, Inscripciones

# 1. IMPORTAR LOS BLUEPRINTS DESDE SUS CARPETAS
from alumnos.routes import alumnos
from maestros.routes import maestros  


import forms_cursos
import forms_inscripciones

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Inicializar extensiones
db.init_app(app)
csrf = CSRFProtect()
csrf.init_app(app) 
migrate = Migrate(app, db)

# 2. REGISTRAR LOS BLUEPRINTS
app.register_blueprint(alumnos)
app.register_blueprint(maestros)   

# ============ RUTA PRINCIPAL ============
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

# ============ RUTAS PARA CURSOS ============
@app.route("/cursos")
def lista_cursos():
    cursos = Cursos.query.all()
    return render_template("cursos/lista_cursos.html", cursos=cursos)

@app.route("/cursos/nuevo", methods=['GET', 'POST'])
def nuevo_curso():
    form = forms_cursos.CursoForm(request.form)
    form.maestro_id.choices = [(0, 'Seleccione un maestro')] + [(m.matricula, f"{m.nombre} {m.apaterno} {m.amaterno}") for m in Maestros.query.all()]
    
    if request.method == 'POST' and form.validate():
        try:
            curso = Cursos(
                nombre_curso=form.nombre_curso.data,
                maestro_id=form.maestro_id.data
            )
            db.session.add(curso)
            db.session.commit()
            flash('Curso registrado exitosamente', 'success')
            return redirect(url_for('lista_cursos.'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'danger')
    return render_template("cursos/curso_form.html", form=form)

@app.route("/cursos/editar/<int:id>", methods=['GET', 'POST'])
def editar_curso(id):
    curso = Cursos.query.get_or_404(id)
    form = forms_cursos.CursoForm(request.form, obj=curso)
    form.maestro_id.choices = [(0, 'Seleccione un maestro')] + [(m.matricula, f"{m.nombre} {m.apaterno} {m.amaterno}") for m in Maestros.query.all()]
    
    if request.method == 'POST' and form.validate():
        try:
            curso.nombre_curso = form.nombre_curso.data
            curso.maestro_id = form.maestro_id.data
            db.session.commit()
            flash('Curso actualizado exitosamente', 'success')
            return redirect(url_for('lista_cursos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    return render_template("cursos/curso_form.html", form=form, curso=curso)

@app.route("/cursos/eliminar/<int:id>")
def eliminar_curso(id):
    try:
        curso = Cursos.query.get_or_404(id)
        db.session.delete(curso)
        db.session.commit()
        flash('Curso eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    return redirect(url_for('lista_cursos'))

# ============ RUTAS PARA INSCRIPCIONES ============
@app.route("/inscripciones")
def lista_inscripciones():
    inscripciones = Inscripciones.query.all()
    return render_template("inscripciones/lista_inscripciones.html", inscripciones=inscripciones)

@app.route("/inscripciones/nueva", methods=['GET', 'POST'])
def nueva_inscripcion():
    form = forms_inscripciones.InscripcionForm(request.form)
    form.alumno_id.choices = [(0, 'Seleccione un alumno')] + [(a.id, f"{a.nombre} {a.apaterno} {a.amaterno}") for a in Alumnos.query.all()]
    form.curso_id.choices = [(0, 'Seleccione un curso')] + [(c.id, c.nombre_curso) for c in Cursos.query.all()]
    
    if request.method == 'POST' and form.validate():
        try:
            existe = Inscripciones.query.filter_by(
                alumno_id=form.alumno_id.data,
                curso_id=form.curso_id.data
            ).first()
            
            if existe:
                flash('El alumno ya está inscrito en este curso', 'warning')
            else:
                inscripcion = Inscripciones(
                    alumno_id=form.alumno_id.data,
                    curso_id=form.curso_id.data
                )
                db.session.add(inscripcion)
                db.session.commit()
                flash('Inscripción realizada exitosamente', 'success')
                return redirect(url_for('lista_inscripciones'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al inscribir: {str(e)}', 'danger')
    
    return render_template("inscripciones/inscripcion_form.html", form=form)

@app.route("/inscripciones/eliminar/<int:id>")
def eliminar_inscripcion(id):
    try:
        inscripcion = Inscripciones.query.get_or_404(id)
        db.session.delete(inscripcion)
        db.session.commit()
        flash('Inscripción eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    return redirect(url_for('lista_inscripciones'))

if __name__ == "__main__":
    app.run(debug=True)