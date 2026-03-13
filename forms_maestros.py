from wtforms import Form
from wtforms import StringField, IntegerField, EmailField
from wtforms import validators

class MaestroForm(Form):
    matricula = IntegerField('Matrícula')
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido')
    ])
    apellidos = StringField('Apellidos', [
        validators.DataRequired(message='Los apellidos son requeridos')
    ])
    especialidad = StringField('Especialidad', [
        validators.DataRequired(message='La especialidad es requerida')
    ])
    email = EmailField('Email', [
        validators.DataRequired(message='El email es requerido'),
        validators.Email(message='Email inválido')
    ])