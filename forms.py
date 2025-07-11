from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField, SubmitField 
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from models import TipoUsuario, Departamento, PeriodoLetivo, Professor

class FormularioLogin(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])
    enviar = SubmitField('Entrar')

class FormularioTipoUsuario(FlaskForm):
    tipo_usuario = SelectField('Tipo de Usuário', coerce=int,
        choices=[(1, 'Aluno'), (2, 'Administrador'), (3, 'Professor'),
                 (4, 'Departamento'), (5, 'Técnico Administrativo')],
        validators=[DataRequired(message='Tipo de usuário é obrigatório')]
    )
    continuar = SubmitField('Continuar')

class FormularioCadastro(FlaskForm):
    nome = StringField('Nome Completo', validators=[
    ])
    email = StringField('Email', validators=[
    ])
    telefone = StringField('Telefone', validators=[
        Length(max=20, message='Telefone deve ter no máximo 20 caracteres')
    ])
    matricula = StringField('Matrícula', validators=[
        Length(max=20, message='Matrícula deve ter no máximo 20 caracteres')
    ])
    senha = PasswordField('Senha', validators=[
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        EqualTo('senha', message='As senhas devem ser iguais')
    ])
    enviar = SubmitField('Cadastrar')
    

class FormularioFeedback(FlaskForm):
    periodo = SelectField('Período Letivo', coerce=int, validators=[
        DataRequired(message='Período é obrigatório')
    ])
    disciplina = SelectField('Disciplina', coerce=str, validators=[
        DataRequired(message='Disciplina é obrigatória')
    ])
    professor = SelectField('Professor', coerce=int, validators=[
    ])
    turma = SelectField('Turma', coerce=int, validators=[
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
    tipo_avaliacao = SelectField('Tipo de avaliação', coerce=int, choices=[
        (0, 'Selecione o tipo de avaliação'),
        (1, 'Prova'),
        (2, 'Trabalho'),
        (3, 'Plano de Ensino'),
        (4, 'Projeto'),
        (5, 'Apresentação')
    ])
    arquivo_pdf = FileField('Documento PDF (opcional)', validators=[
        FileAllowed(['pdf'], 'Apenas arquivos PDF são permitidos!')
    ])
    enviar = SubmitField('Enviar Feedback')
    
    def __init__(self, *args, **kwargs):
        super(FormularioFeedback, self).__init__(*args, **kwargs)
        from models import PeriodoLetivo, Disciplina, Professor
        
        # Inicializar choices vazias (serão preenchidas via AJAX)
        self.periodo.choices = [(0, 'Carregando períodos...')]
        self.disciplina.choices = [(0, 'Carregando disciplinas...')]
        self.professor.choices = [(0, 'Selecione primeiro uma turma')]
        self.turma.choices = [(0, 'Selecione período e disciplina primeiro')]
        
        # Carregar dados se estiver disponível
        try:
            periodos_ordenados = PeriodoLetivo.query.order_by(PeriodoLetivo.ano_periodo.desc(), PeriodoLetivo.sequencial_periodo.desc()).all()
            self.periodo.choices = [(0, 'Selecione um período')] + [(p.codigo_periodo, f"{p.ano_periodo}.{p.sequencial_periodo}") for p in periodos_ordenados]
            
            disciplinas_ordenadas = Disciplina.query.order_by(Disciplina.nome_disciplina).all()
            self.disciplina.choices = [(0, 'Selecione uma disciplina')] + [(d.codigo_disciplina, f"{d.codigo_disciplina} - {d.nome_disciplina}") for d in disciplinas_ordenadas]
        except:
            # Em caso de erro, manter choices vazias
            pass

class FormularioDisciplina(FlaskForm):
    codigo_disciplina = StringField('Código da Disciplina', validators=[
        DataRequired(message='Código da disciplina é obrigatório'),
        Length(max=10, message='Código deve ter no máximo 10 caracteres')
    ])

    departamento = SelectField('Departamento', validators=[
        DataRequired(message='Departamento é obrigatório')
    ])

    nome_disciplina = StringField('Nome da Disciplina', validators=[
        DataRequired(message='Nome da disciplina é obrigatório'),
        Length(max=100, message='Nome deve ter no máximo 100 caracteres')
    ])

    enviar = SubmitField('Cadastrar Disciplina')

    def __init__(self, *args, **kwargs):
        super(FormularioDisciplina, self).__init__(*args, **kwargs)
        self.departamento.choices = [(d.codigo_departamento, d.nome_departamento) for d in Departamento.query.all()]
class FormularioProfessorNovo(FlaskForm):
    codigo_professor = IntegerField('Código do Professor', validators=[
        DataRequired(message='Código do professor é obrigatório'),
        NumberRange(min=1, message='Código deve ser um número positivo')
    ])
    nome_professor = StringField('Nome do Professor', validators=[
        DataRequired(message='Nome do professor é obrigatório'),
        Length(min=2, max=25, message='Nome deve ter entre 2 e 25 caracteres')
    ])
    enviar = SubmitField('Salvar Professor')

class FormularioProfessor(FlaskForm):
    nome = StringField('Nome Completo', validators=[
    ])
    email = StringField('Email', validators=[
    ])
    telefone = StringField('Telefone', validators=[
        Length(max=20, message='Telefone deve ter no máximo 20 caracteres')
    ])
    matricula = StringField('Matrícula', validators=[
        Length(max=20, message='Matrícula deve ter no máximo 20 caracteres')
    ])
    senha = PasswordField('Senha', validators=[
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        EqualTo('senha', message='As senhas devem ser iguais')
    ])
    codigo_professor = IntegerField('Código do Professor', validators=[
    ])
    nome_professor = StringField('Nome do Professor', validators=[
    ])
    professor_existente = SelectField('Selecione seu perfil de professor', coerce=int, validators=[], choices=[])

    enviar = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(FormularioProfessor, self).__init__(*args, **kwargs)
        professores = Professor.query.order_by(Professor.nome_professor).all()
        self.professor_existente.choices = [(p.codigo_professor, p.nome_professor) for p in professores]


class FormularioTurma(FlaskForm):
    numero_identificacao_turma = IntegerField('Número da Turma', validators=[
        DataRequired(message='Número da turma é obrigatório'),
        NumberRange(min=1, message='Número deve ser um número positivo')
    ])
    disciplina = SelectField('Disciplina', coerce=str, validators=[
        DataRequired(message='Disciplina é obrigatória')
    ], choices=[])
    periodo = SelectField('Período', coerce=str, validators=[
        DataRequired(message='Período é obrigatório')
    ], choices=[])
    professor = SelectField('Professor (opcional)', coerce=int, validators=[], choices=[])
    enviar = SubmitField('Salvar Turma')
    
    def __init__(self, *args, **kwargs):
        super(FormularioTurma, self).__init__(*args, **kwargs)
        from models import Disciplina, PeriodoLetivo, Professor
        
        # Carregar disciplinas
        disciplinas = Disciplina.query.order_by(Disciplina.nome_disciplina).all()
        self.disciplina.choices = [(d.codigo_disciplina, f"{d.codigo_disciplina} - {d.nome_disciplina}") for d in disciplinas]
        
        # Carregar períodos
        periodos = PeriodoLetivo.query.order_by(PeriodoLetivo.ano_periodo.desc(), PeriodoLetivo.sequencial_periodo.desc()).all()
        self.periodo.choices = [(f"{p.ano_periodo}.{p.sequencial_periodo}", f"{p.ano_periodo}.{p.sequencial_periodo}") for p in periodos]
        
        # Carregar professores (opcional)
        professores = Professor.query.order_by(Professor.nome_professor).all()
        self.professor.choices = [(0, 'Nenhum professor selecionado')] + [(p.codigo_professor, p.nome_professor) for p in professores]