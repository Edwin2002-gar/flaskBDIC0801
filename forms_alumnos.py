from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Optional

class AlumnoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='El nombre es requerido')])
    apaterno = StringField('Apellido Paterno', validators=[DataRequired(message='El apellido paterno es requerido')])
    amaterno = StringField('Apellido Materno', validators=[Optional()])  # Opcional
    edad = IntegerField('Edad', validators=[DataRequired(message='La edad es requerida'), NumberRange(min=1, max=120, message='Edad inválida')])
    email = EmailField('Email', validators=[DataRequired(message='El email es requerido'), Email(message='Correo inválido')])
    submit = SubmitField('Guardar Alumno')