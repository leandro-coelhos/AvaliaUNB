from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class UsuarioForm(FlaskForm):
     nome = StringField('Nome', validators=[DataRequired()])
     email = StringField('Email', validators=[DataRequired()])
     telefone = StringField('Telefone', validators=[DataRequired()])
     matricula = StringField('Matrícula', validators=[DataRequired()])
     tipo_usuario = SelectField('Tipo de Usuário', choices=[(0, 'Aluno'), (1, 'Administrador')], validators=[DataRequired()])

     submit = SubmitField('Enviar')
     cancel = SubmitField('Cancelar')
     delete = SubmitField('Excluir')
     edit = SubmitField('Editar')

     def __init__(self, *args, **kwargs):
          super(UsuarioForm, self).__init__(*args, **kwargs)
          # Additional initialization if needed