from flask_wtf import FlaskForm
from wtforms import Form, SelectField, SubmitField
from wtforms.validators import DataRequired

class InscripcionForm(Form):
    alumno_id = SelectField('Alumno', coerce=int, validators=[DataRequired()])
    curso_id = SelectField('Curso', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Inscribir')