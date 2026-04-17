# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apaterno = db.Column(db.String(100), nullable=False)
    amaterno = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(200), nullable=False)
    
    def __init__(self, nombre, apaterno, amaterno, edad, email):
        self.nombre = nombre
        self.apaterno = apaterno
        self.amaterno = amaterno
        self.edad = edad
        self.email = email

class Maestros(db.Model):
    __tablename__ = 'maestros'
    matricula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    apellidos = db.Column(db.String(200))  # ← Cambiado: un solo campo
    email = db.Column(db.String(100), unique=True)
    especialidad = db.Column(db.String(100))
    # telefono no existe en tu tabla según la imagen
    
    def __init__(self, nombre, apellidos, email, especialidad):
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.especialidad = especialidad

class Cursos(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_curso = db.Column(db.String(200), nullable=False)
    maestro_id = db.Column(db.Integer, db.ForeignKey('maestros.matricula'), nullable=False)
    
    maestro = db.relationship('Maestros', backref='cursos', lazy=True)
    
    def __init__(self, nombre_curso, maestro_id):
        self.nombre_curso = nombre_curso
        self.maestro_id = maestro_id

class Inscripciones(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    
    alumno = db.relationship('Alumnos', backref='inscripciones', lazy=True)
    curso = db.relationship('Cursos', backref='inscripciones', lazy=True)
    
    def __init__(self, alumno_id, curso_id):
        self.alumno_id = alumno_id
        self.curso_id = curso_id

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(50), default='usuario')
    
    def __init__(self, username, password, rol='usuario'):
        self.username = username
        self.password = password
        self.rol = rol