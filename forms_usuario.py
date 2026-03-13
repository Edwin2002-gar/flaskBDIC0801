from wtforms import Form
from wtforms import StringField, IntegerField, EmailField
from wtforms import validators

class UsuarioForm(Form):
    matricula = IntegerField('Matrícula')
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido')
    ])
    apellidos = StringField('Apellidos', [
        validators.DataRequired(message='Los apellidos son requeridos')
    ])
    correo = EmailField('Correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Correo inválido')
    ])