from flask_sqlalchemy import SQLAlchemy
import datetime

db= SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apaterno = db.Column(db.String(50), nullable=False)
    amaterno = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    edad = db.Column(db.Date, nullable=False)

    def __init__(self, nombre, apaterno, amaterno, email, edad):
        self.nombre = nombre
        self.apaterno = apaterno
        self.amaterno = amaterno
        self.email = email
        self.edad = edad