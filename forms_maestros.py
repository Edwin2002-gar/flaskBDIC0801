from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email

class MaestroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='El nombre es requerido')])
    apellidos = StringField('Apellidos', validators=[DataRequired(message='Los apellidos son requeridos')])
    email = EmailField('Email', validators=[DataRequired(message='El email es requerido'), Email(message='Email inválido')])
    especialidad = StringField('Especialidad', validators=[DataRequired(message='La especialidad es requerida')])
    submit = SubmitField('Guardar Maestro')