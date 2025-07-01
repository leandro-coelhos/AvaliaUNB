from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, DateField, SubmitField
from wtforms.validators import DataRequired

class PeriodoForm(FlaskForm):
     id = StringField('ID', validators=[DataRequired()])
     ano = IntegerField('Ano', validators=[DataRequired()])
     sequencial = IntegerField('Sequencial', validators=[DataRequired()])
     SubmitField('Enviar')
     SubmitField('Cancelar')
     SubmitField('Excluir')
     SubmitField('Editar')

     def __init__(self, *args, **kwargs):
          super(PeriodoForm, self).__init__(*args, **kwargs)
          # Additional initialization if needed