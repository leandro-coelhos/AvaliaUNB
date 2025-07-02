
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from models import TipoUsuario

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=2, max=25, message='Nome deve ter entre 2 e 25 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido'),
        Length(max=35, message='Email deve ter no máximo 35 caracteres')
    ])
    telefone = StringField('Telefone', validators=[
        DataRequired(message='Telefone é obrigatório'),
        Length(max=20, message='Telefone deve ter no máximo 20 caracteres')
    ])
    matricula = StringField('Matrícula', validators=[
        DataRequired(message='Matrícula é obrigatória'),
        Length(max=20, message='Matrícula deve ter no máximo 20 caracteres')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Senha deve ter pelo menos 6 caracteres')
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='Confirmação de senha é obrigatória'),
        EqualTo('senha', message='As senhas devem ser iguais')
    ])
    tipo_usuario = SelectField('Tipo de Usuário', coerce=int,
        choices=[('1', 'Aluno'), ('2', 'Administrador')],
        validators=[DataRequired(message='Tipo de usuário é obrigatório')]
    )
    submit = SubmitField('Cadastrar')

class FeedbackForm(FlaskForm):
    professor = SelectField('Professor', coerce=int, validators=[
        DataRequired(message='Professor é obrigatório')
    ])
    turma = SelectField('Turma', coerce=int, validators=[
        DataRequired(message='Turma é obrigatória')
    ])
    dificuldade = IntegerField('Nível de Dificuldade (1-5)', validators=[
        DataRequired(message='Nível de dificuldade é obrigatório'),
        NumberRange(min=1, max=5, message='Nível de dificuldade deve ser entre 1 e 5')
    ])
    qualidade = IntegerField('Qualidade (1-5)', validators=[
        DataRequired(message='Qualidade é obrigatória'),
        NumberRange(min=1, max=5, message='Qualidade deve ser entre 1 e 5')
    ])
    comentario = TextAreaField('Comentário', validators=[
        DataRequired(message='Comentário é obrigatório'),
        Length(min=1, max=100, message='Comentário deve ter no máximo 100 caracteres')
    ])
    submit = SubmitField('Enviar Feedback')
