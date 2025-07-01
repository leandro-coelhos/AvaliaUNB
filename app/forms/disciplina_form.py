from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class PeriodoForm(FlaskForm):
     id = StringField('ID', validators=[DataRequired()])
     nome = StringField('Nome', validators=[DataRequired()])
     departamento = SelectField('Departamento', validators=[DataRequired()])
     programa = FileField('Programa', validators=[FileRequired(), FileAllowed(['pdf'], 'PDFs only!')])
     SubmitField('Enviar')
     SubmitField('Cancelar')
     SubmitField('Excluir')
     SubmitField('Editar')
