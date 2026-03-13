from wtforms import Form
from wtforms import StringField, IntegerField, EmailField
from wtforms import validators

class UsarForm(Form):
    id = IntegerField('ID')
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido')
    ])
    apaterno = StringField('Apellido Paterno', [
        validators.DataRequired(message='El apellido paterno es requerido')
    ])
    amaterno = StringField('Apellido Materno')
    edad = IntegerField('Edad', [
        validators.NumberRange(min=1, max=100, message='Edad inválida')
    ])
    correo = EmailField('Correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Correo inválido')
    ])