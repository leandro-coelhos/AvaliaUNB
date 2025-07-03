
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from models import TipoUsuario

class FormularioLogin(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])
    enviar = SubmitField('Entrar')

class FormularioCadastro(FlaskForm):
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
    enviar = SubmitField('Cadastrar')

class FormularioFeedback(FlaskForm):
    professor = SelectField('Professor', coerce=int, validators=[
        DataRequired(message='Professor é obrigatório')
    ])
    turma = SelectField('Turma', coerce=int, validators=[
        DataRequired(message='Turma é obrigatória')
    ])
    dificuldade = SelectField('Nível de Dificuldade', coerce=int, choices=[
        (1, '1 - Muito Fácil'),
        (2, '2 - Fácil'),
        (3, '3 - Moderado'),
        (4, '4 - Difícil'),
        (5, '5 - Muito Difícil')
    ], validators=[
        DataRequired(message='Nível de dificuldade é obrigatório')
    ])
    qualidade = SelectField('Qualidade', coerce=int, choices=[
        (1, '1 - Muito Ruim'),
        (2, '2 - Ruim'),
        (3, '3 - Regular'),
        (4, '4 - Bom'),
        (5, '5 - Excelente')
    ], validators=[
        DataRequired(message='Qualidade é obrigatória')
    ])
    comentario = TextAreaField('Comentário', validators=[
        DataRequired(message='Comentário é obrigatório'),
        Length(min=1, max=100, message='Comentário deve ter no máximo 100 caracteres')
    ])
    tipo_documento = SelectField('Tipo de Documento', choices=[
        ('', 'Selecione o tipo (opcional)'),
        ('prova', 'Prova'),
        ('plano_ensino', 'Plano de Ensino'),
        ('slide', 'Slide/Apresentação'),
        ('material_apoio', 'Material de Apoio'),
        ('outro', 'Outro')
    ])
    arquivo_pdf = FileField('Documento PDF (opcional)', validators=[
        FileAllowed(['pdf'], 'Apenas arquivos PDF são permitidos!')
    ])
    enviar = SubmitField('Enviar Feedback')
