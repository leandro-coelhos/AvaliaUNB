
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class FormularioCriterio(FlaskForm):
     identificacao = StringField('ID', validators=[DataRequired()])
     turma = SelectField('Turma', validators=[DataRequired()])
     tipo_avaliacao = SelectField('Tipo de Avaliação', validators=[DataRequired()])
     
     enviar = SubmitField('Enviar')
     cancelar = SubmitField('Cancelar')
     excluir = SubmitField('Excluir')
     editar = SubmitField('Editar')
     
     def __init__(self, *args, **kwargs):
          super(FormularioCriterio, self).__init__(*args, **kwargs)
          # Inicialização adicional se necessário
