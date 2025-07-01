from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class TipoAvaliacaoForm(FlaskForm):
     id = StringField('ID', validators=[DataRequired()])
     nome = StringField('Nome', validators=[DataRequired()])
     
     submit = SubmitField('Enviar')
     cancel = SubmitField('Cancelar')
     delete = SubmitField('Excluir')
     edit = SubmitField('Editar')