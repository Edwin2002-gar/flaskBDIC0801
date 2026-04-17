from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CursoForm(FlaskForm):
    nombre_curso = StringField('Nombre del Curso', validators=[DataRequired(message='El nombre del curso es requerido')])
    maestro_id = SelectField('Maestro Asignado', coerce=int, validators=[DataRequired(message='Debe seleccionar un maestro')])
    submit = SubmitField('Guardar Curso')