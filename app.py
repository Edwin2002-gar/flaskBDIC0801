from flask import Flask, render_template,request, redirect, url_for
import forms
from flask_wtf.csrf import CSRFProtect
from flask import flash
from config import DevelopmentConfig


from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf = CSRFProtect(app)



@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/usuarios", methods=["GET","POST"])
def usuario():
	mat=0
	nom=''
	apa=''
	ama=''
	edad=0
	email=''
	usuarios_clas=forms.UsarForm(request.form)
	if request.method== 'POST':
		mat=usuarios_clas.matricula.data
		nom=usuarios_clas.nombre.data
		apa=usuarios_clas.apaterno.data
		ama=usuarios_clas.amaterno.data
		edad=usuarios_clas.edad.data
		email=usuarios_clas.correo.data

	return render_template('usuarios.html', form=usuarios_clas,mat=mat,
						nom=nom,apa=apa,ama=ama,edad=edad,email=email)


if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()