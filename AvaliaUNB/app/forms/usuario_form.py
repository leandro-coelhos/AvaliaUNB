
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class FormularioUsuario(FlaskForm):
     nome = StringField('Nome', validators=[DataRequired()])
     email = StringField('Email', validators=[DataRequired()])
     telefone = StringField('Telefone', validators=[DataRequired()])
     matricula = StringField('Matrícula', validators=[DataRequired()])
     tipo_usuario = SelectField('Tipo de Usuário', choices=[(0, 'Aluno'), (1, 'Administrador')], validators=[DataRequired()])

     enviar = SubmitField('Enviar')
     cancelar = SubmitField('Cancelar')
     excluir = SubmitField('Excluir')
     editar = SubmitField('Editar')

     def __init__(self, *args, **kwargs):
          super(FormularioUsuario, self).__init__(*args, **kwargs)
          # Inicialização adicional se necessário
