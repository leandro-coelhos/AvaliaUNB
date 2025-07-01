from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, DateField, SubmitField
from wtforms.validators import DataRequired

class TurmaForm(FlaskForm):
     id = IntegerField('ID', validators=[DataRequired()])
     disciplina = SelectMultipleField('Disciplina', validators=[DataRequired()])
     periodo = SelectMultipleField('Período', validators=[DataRequired()])
     SubmitField('Enviar')
     SubmitField('Cancelar')
     SubmitField('Excluir')
     SubmitField('Editar')

     def __init__(self, *args, **kwargs):
         super(TurmaForm, self).__init__(*args, **kwargs)
         self.disciplina.choices = getDisciplinas()
         self.periodo.choices = getPeriodos()