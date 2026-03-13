from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define todos los modelos aquí
class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apaterno = db.Column(db.String(250), nullable=False)
    amaterno = db.Column(db.String(250))
    edad = db.Column(db.Integer)
    email = db.Column(db.String(250), unique=True, nullable=False)

class Maestros(db.Model):
    __tablename__ = 'maestros'
    matricula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(200), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    matricula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(200), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)