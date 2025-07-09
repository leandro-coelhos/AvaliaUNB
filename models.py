
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Departamento(db.Model):
    __tablename__ = 'Dep'
    
    codigo_departamento = db.Column('Cod_Dep', db.String(10), primary_key=True)
    nome_departamento = db.Column('Nom_Dep', db.String(25))
    
    disciplinas = db.relationship('Disciplina', backref='departamento', lazy=True)

class Disciplina(db.Model):
    __tablename__ = 'Dis'
    
    codigo_disciplina = db.Column('Cod_Dis', db.String(10), primary_key=True)
    nome_disciplina = db.Column('Nom_Dis', db.String(25))
    fk_codigo_departamento = db.Column('fk_Cod_Dep', db.String(10), db.ForeignKey('Dep.Cod_Dep'), nullable=False)
    programa_disciplina = db.Column('Prog_Dis', db.LargeBinary)
    
    turmas = db.relationship('Turma', backref='disciplina', lazy=True)

class Professor(db.Model):
    __tablename__ = 'Prof'
    
    codigo_professor = db.Column('Cod_Prof', db.SmallInteger, primary_key=True)
    nome_professor = db.Column('Nom_Prof', db.String(25))
    
    feedbacks = db.relationship('Feedback', backref='professor', lazy=True)

class TipoUsuario(db.Model):
    __tablename__ = 'Tp_Usr'
    
    codigo_tipo_usuario = db.Column('Cod_Tp_Usr', db.SmallInteger, primary_key=True)
    nome_tipo_usuario = db.Column('Nom_Tp_Usr', db.String(25))
    
    usuarios = db.relationship('Usuario', backref='tipo_usuario', lazy=True)

class Usuario(db.Model):
    __tablename__ = 'Usr'
    
    numero_identificacao_usuario = db.Column('Num_Idf_Usr', db.Integer, primary_key=True)
    nome_usuario = db.Column('Nom_Usr', db.String(25))
    email_usuario = db.Column('Email_Usr', db.String(35))
    telefone_usuario = db.Column('Tel_Usr', db.String(20))
    matricula_usuario = db.Column('Mat_Usr', db.String(20))
    senha_usuario = db.Column('Senha_Usr', db.String(255))
    fk_codigo_tipo_usuario = db.Column('fk_Cod_Tp_Usr', db.SmallInteger, db.ForeignKey('Tp_Usr.Cod_Tp_Usr'), nullable=False)
    
    feedbacks = db.relationship('Feedback', backref='usuario', lazy=True)

class PeriodoLetivo(db.Model):
    __tablename__ = 'Per_Let'
    
    codigo_periodo = db.Column('Cod_Per', db.Integer, primary_key=True, autoincrement=True)
    ano_periodo = db.Column('Ano_Per', db.SmallInteger)
    sequencial_periodo = db.Column('Seq_Per', db.SmallInteger)
    
    turmas = db.relationship('Turma', backref='periodo', lazy=True)

class Turma(db.Model):
    __tablename__ = 'Tur'
    
    numero_identificacao_turma = db.Column('Num_Idf_Tur', db.SmallInteger, primary_key=True)
    fk_codigo_disciplina = db.Column('fk_Cod_Dis', db.String(10), db.ForeignKey('Dis.Cod_Dis'), nullable=False)
    fk_codigo_periodo = db.Column('fk_Cod_Per', db.String(10), db.ForeignKey('Per_Let.Cod_Per'), nullable=False)
    
    criterios_avaliacao = db.relationship('CriterioAvaliacaoTurma', backref='turma', lazy=True)
    feedbacks = db.relationship('Feedback', backref='turma', lazy=True)

class TipoAvaliacao(db.Model):
    __tablename__ = 'Tp_Aval'
    
    codigo_tipo_avaliacao = db.Column('Cod_Tp_Aval', db.SmallInteger, primary_key=True)
    nome_tipo_avaliacao = db.Column('Nom_Tp_Aval', db.String(25))
    
    criterios_avaliacao = db.relationship('CriterioAvaliacaoTurma', backref='tipo_avaliacao', lazy=True)

class CriterioAvaliacaoTurma(db.Model):
    __tablename__ = 'Crit_Aval_Tur'
    
    numero_identificacao_avaliacao = db.Column('Num_Idf_Aval', db.Integer, primary_key=True)
    fk_numero_identificacao_turma = db.Column('fk_Num_Idf_Tur', db.SmallInteger, db.ForeignKey('Tur.Num_Idf_Tur'), nullable=False)
    fk_codigo_tipo_avaliacao = db.Column('fk_Cod_Tp_Aval', db.SmallInteger, db.ForeignKey('Tp_Aval.Cod_Tp_Aval'), nullable=False)
    
    documentos = db.relationship('DocumentoAvaliacao', backref='criterio_avaliacao', lazy=True)

class DocumentoAvaliacao(db.Model):
    __tablename__ = 'Doc_Aval'
    
    numero_identificacao_documento = db.Column('Num_Idf_Doc', db.Integer, primary_key=True)
    arquivo_documento = db.Column('Arq_Doc', db.LargeBinary)
    nome_arquivo = db.Column('Nome_Arq', db.String(255))
    tipo_documento = db.Column('Tipo_Doc', db.String(50))
    fk_numero_identificacao_avaliacao = db.Column('fk_Num_Idf_Aval', db.Integer, db.ForeignKey('Crit_Aval_Tur.Num_Idf_Aval'), nullable=False)
    # Campos adicionais para associar ao feedback específico
    fk_usuario_id = db.Column('fk_Usr_Id', db.Integer, db.ForeignKey('Usr.Num_Idf_Usr'), nullable=True)
    fk_professor_id = db.Column('fk_Prof_Id', db.SmallInteger, db.ForeignKey('Prof.Cod_Prof'), nullable=True)
    fk_turma_id = db.Column('fk_Tur_Id', db.SmallInteger, db.ForeignKey('Tur.Num_Idf_Tur'), nullable=True)

class Feedback(db.Model):
    __tablename__ = 'Fdbk'
    
    pfk_numero_identificacao_turma = db.Column('pfk_Num_Idf_Tur', db.SmallInteger, db.ForeignKey('Tur.Num_Idf_Tur'), primary_key=True)
    pfk_codigo_professor = db.Column('pfk_Cod_Prof', db.SmallInteger, db.ForeignKey('Prof.Cod_Prof'), primary_key=True)
    pfk_numero_identificacao_usuario = db.Column('pfk_Num_Idf_Usr', db.Integer, db.ForeignKey('Usr.Num_Idf_Usr'), primary_key=True)
    nivel_dificuldade = db.Column('Nvl_Dif', db.SmallInteger)
    qualidade = db.Column('Qual', db.SmallInteger)
    comentario = db.Column('Coment', db.String(100))
