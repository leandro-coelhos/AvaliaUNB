from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DepartamentoForm(FlaskForm):
     id = StringField('ID', validators=[DataRequired()])
     nome = StringField('Nome', validators=[DataRequired()])
     SubmitField('Enviar')
     SubmitField('Cancelar')
     SubmitField('Excluir')
     SubmitField('Editar')
     