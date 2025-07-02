from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField, IntegerField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired

class DocumentoForm(FlaskForm):
     id = IntegerField('ID', validators=[DataRequired()])
     file = FileField('Arquivo', validators=[FileRequired(), FileAllowed(['pdf'], 'Apenas PDFs!')])
     avaliacao = SelectField('Avaliação', validators=[DataRequired()])
     
     
     submit = SubmitField('Enviar')
     cancel = SubmitField('Cancelar')
     delete = SubmitField('Excluir')
     edit = SubmitField('Editar')
     
     def __init__(self, *args, **kwargs):
          super(DocumentoForm, self).__init__(*args, **kwargs)
          # Additional initialization if needed