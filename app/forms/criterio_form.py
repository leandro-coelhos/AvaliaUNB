from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class CriterioForm(FlaskForm):
     id = StringField('ID', validators=[DataRequired()])
     turma = SelectField('Turma', validators=[DataRequired()])
     tipo_avaliacao = SelectField('Tipo de Avaliação', validators=[DataRequired()])
     
     submit = SubmitField('Enviar')
     cancel = SubmitField('Cancelar')
     delete = SubmitField('Excluir')
     edit = SubmitField('Editar')
     
     def __init__(self, *args, **kwargs):
          super(CriterioForm, self).__init__(*args, **kwargs)
          # Additional initialization if needed