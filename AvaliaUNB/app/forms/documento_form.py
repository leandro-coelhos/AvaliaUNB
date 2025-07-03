
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField, IntegerField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired

class FormularioDocumento(FlaskForm):
     identificacao = IntegerField('ID', validators=[DataRequired()])
     arquivo = FileField('Arquivo', validators=[FileRequired(), FileAllowed(['pdf'], 'Apenas PDFs!')])
     avaliacao = SelectField('Avaliação', validators=[DataRequired()])
     
     enviar = SubmitField('Enviar')
     cancelar = SubmitField('Cancelar')
     excluir = SubmitField('Excluir')
     editar = SubmitField('Editar')
     
     def __init__(self, *args, **kwargs):
          super(FormularioDocumento, self).__init__(*args, **kwargs)
