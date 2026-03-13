from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig


from models import db, Alumnos, Maestros, Usuarios

# Importar formularios
import forms_alumnos
import forms_maestros
import forms_usuario

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
migrate= Migrate(app, db)
csrf = CSRFProtect(app)

# ============================================
# RUTAS PARA ALUMNOS
# ============================================

@app.route("/")
@app.route("/index")
def index():
    create_form = forms_alumnos.UsarForm(request.form)
    alumnos = Alumnos.query.all()
    return render_template("index_alumnos.html", form=create_form, alumnos=alumnos)

@app.route("/alumnos/nuevo", methods=["GET", "POST"])
def alumnos_nuevo():
    form = forms_alumnos.UsarForm(request.form)
    if request.method == 'POST' and form.validate():
        alumno = Alumnos(
            nombre=form.nombre.data,
            apaterno=form.apaterno.data,
            amaterno=form.amaterno.data,
            edad=form.edad.data,
            email=form.correo.data
        )
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('alumnos_form.html', form=form)

@app.route("/alumnos/editar/<int:id>", methods=["GET", "POST"])
def alumnos_editar(id):
    alumno = Alumnos.query.get_or_404(id)
    form = forms_alumnos.UsarForm(request.form, obj=alumno)
    if request.method == 'POST' and form.validate():
        alumno.nombre = form.nombre.data
        alumno.apaterno = form.apaterno.data
        alumno.amaterno = form.amaterno.data
        alumno.edad = form.edad.data
        alumno.email = form.correo.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('alumnos_form.html', form=form)

@app.route("/alumnos/eliminar/<int:id>")
def alumnos_eliminar(id):
    alumno = Alumnos.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    return redirect(url_for('index'))

# ============================================
# RUTAS PARA MAESTROS
# ============================================

@app.route("/maestros")
def maestros_lista():
    maestros = Maestros.query.all()
    return render_template("maestros_lista.html", maestros=maestros)

@app.route("/maestros/nuevo", methods=["GET", "POST"])
def maestros_nuevo():
    form = forms_maestros.MaestroForm(request.form)
    if request.method == 'POST' and form.validate():
        maestro = Maestros(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            especialidad=form.especialidad.data,
            email=form.email.data
        )
        db.session.add(maestro)
        db.session.commit()
        return redirect(url_for('maestros_lista'))
    return render_template('maestro_form.html', form=form)

@app.route("/maestros/editar/<int:matricula>", methods=["GET", "POST"])
def maestros_editar(matricula):
    maestro = Maestros.query.get_or_404(matricula)
    form = forms_maestros.MaestroForm(request.form, obj=maestro)
    if request.method == 'POST' and form.validate():
        maestro.nombre = form.nombre.data
        maestro.apellidos = form.apellidos.data
        maestro.especialidad = form.especialidad.data
        maestro.email = form.email.data
        db.session.commit()
        return redirect(url_for('maestros_lista'))
    return render_template('maestro_form.html', form=form)

@app.route("/maestros/eliminar/<int:matricula>")
def maestros_eliminar(matricula):
    maestro = Maestros.query.get_or_404(matricula)
    db.session.delete(maestro)
    db.session.commit()
    return redirect(url_for('maestros_lista'))

# ============================================
# RUTAS PARA USUARIOS
# ============================================

@app.route("/usuarios")
def usuarios_lista():
    usuarios = Usuarios.query.all()
    return render_template("usuario_lista.html", usuarios=usuarios)

@app.route("/usuarios/nuevo", methods=["GET", "POST"])
def usuarios_nuevo():
    form = forms_usuario.UsuarioForm(request.form)
    if request.method == 'POST' and form.validate():
        usuario = Usuarios(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            correo=form.correo.data
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuarios_lista'))
    return render_template('usuario_form.html', form=form)

@app.route("/usuarios/editar/<int:matricula>", methods=["GET", "POST"])
def usuarios_editar(matricula):
    usuario = Usuarios.query.get_or_404(matricula)
    form = forms_usuario.UsuarioForm(request.form, obj=usuario)
    if request.method == 'POST' and form.validate():
        usuario.nombre = form.nombre.data
        usuario.apellidos = form.apellidos.data
        usuario.correo = form.correo.data
        db.session.commit()
        return redirect(url_for('usuarios_lista'))
    return render_template('usuario_form.html', form=form)

@app.route("/usuarios/eliminar/<int:matricula>")
def usuarios_eliminar(matricula):
    usuario = Usuarios.query.get_or_404(matricula)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuarios_lista'))

# ============================================
# INICIO DE LA APLICACIÓN
# ============================================

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)