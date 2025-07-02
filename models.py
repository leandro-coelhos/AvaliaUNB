
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Departamento(db.Model):
    __tablename__ = 'Dep'
    
    Cod_Dep = db.Column(db.String(10), primary_key=True)
    Nom_Dep = db.Column(db.String(25))
    
    # Relacionamentos
    disciplinas = db.relationship('Disciplina', backref='departamento', lazy=True)

class TipoUsuario(db.Model):
    __tablename__ = 'Tp_Usr'
    
    Cod_Tp_Usr = db.Column(db.SmallInteger, primary_key=True)
    Nom_Tp_Usr = db.Column(db.String(25))
    
    # Relacionamentos
    usuarios = db.relationship('Usuario', backref='tipo_usuario', lazy=True)

class TipoAvaliacao(db.Model):
    __tablename__ = 'Tp_Aval'
    
    Cod_Tp_Aval = db.Column(db.SmallInteger, primary_key=True)
    Nom_Tp_Aval = db.Column(db.String(25))
    
    # Relacionamentos
    criterios = db.relationship('CriterioAvaliacaoTurma', backref='tipo_avaliacao', lazy=True)

class PeriodoLetivo(db.Model):
    __tablename__ = 'Per_Let'
    
    Cod_Per = db.Column(db.String(10), primary_key=True)
    Ano_Per = db.Column(db.SmallInteger)
    Seq_Per = db.Column(db.SmallInteger)
    
    # Relacionamentos
    turmas = db.relationship('Turma', backref='periodo_letivo', lazy=True)

class Disciplina(db.Model):
    __tablename__ = 'Dis'
    
    Cod_Dis = db.Column(db.String(10), primary_key=True)
    Nom_Dis = db.Column(db.String(25))
    fk_Cod_Dep = db.Column(db.String(10), db.ForeignKey('Dep.Cod_Dep'), nullable=False)
    Prog_Dis = db.Column(db.LargeBinary)
    
    # Relacionamentos
    turmas = db.relationship('Turma', backref='disciplina', lazy=True)

class Professor(db.Model):
    __tablename__ = 'Prof'
    
    Cod_Prof = db.Column(db.SmallInteger, primary_key=True)
    Nom_Prof = db.Column(db.String(25))
    
    # Relacionamentos
    feedbacks = db.relationship('Feedback', backref='professor', lazy=True)

class Usuario(db.Model):
    __tablename__ = 'Usr'
    
    Num_Idf_Usr = db.Column(db.Integer, primary_key=True)
    Nom_Usr = db.Column(db.String(25))
    Email_Usr = db.Column(db.String(35))
    Tel_Usr = db.Column(db.String(20))
    Mat_Usr = db.Column(db.String(20))
    Senha_Usr = db.Column(db.String(255))  # Campo para senha hashada
    fk_Cod_Tp_Usr = db.Column(db.SmallInteger, db.ForeignKey('Tp_Usr.Cod_Tp_Usr'), nullable=False)
    
    # Relacionamentos
    feedbacks = db.relationship('Feedback', backref='usuario', lazy=True)

class Turma(db.Model):
    __tablename__ = 'Tur'
    
    Num_Idf_Tur = db.Column(db.SmallInteger, primary_key=True)
    fk_Cod_Dis = db.Column(db.String(10), db.ForeignKey('Dis.Cod_Dis'), nullable=False)
    fk_Cod_Per = db.Column(db.String(10), db.ForeignKey('Per_Let.Cod_Per'), nullable=False)
    
    # Relacionamentos
    criterios_avaliacao = db.relationship('CriterioAvaliacaoTurma', backref='turma', lazy=True)
    feedbacks = db.relationship('Feedback', backref='turma', lazy=True)

class CriterioAvaliacaoTurma(db.Model):
    __tablename__ = 'Crit_Aval_Tur'
    
    Num_Idf_Aval = db.Column(db.Integer, primary_key=True)
    fk_Num_Idf_Tur = db.Column(db.SmallInteger, db.ForeignKey('Tur.Num_Idf_Tur'), nullable=False)
    fk_Cod_Tp_Aval = db.Column(db.SmallInteger, db.ForeignKey('Tp_Aval.Cod_Tp_Aval'), nullable=False)
    
    # Relacionamentos
    documentos = db.relationship('DocumentoAvaliacao', backref='criterio_avaliacao', lazy=True)

class DocumentoAvaliacao(db.Model):
    __tablename__ = 'Doc_Aval'
    
    Num_Idf_Doc = db.Column(db.Integer, primary_key=True)
    Arq_Doc = db.Column(db.LargeBinary)
    fk_Num_Idf_Aval = db.Column(db.Integer, db.ForeignKey('Crit_Aval_Tur.Num_Idf_Aval'), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'Fdbk'
    
    pfk_Num_Idf_Tur = db.Column(db.SmallInteger, db.ForeignKey('Tur.Num_Idf_Tur'), primary_key=True)
    pfk_Cod_Prof = db.Column(db.SmallInteger, db.ForeignKey('Prof.Cod_Prof'), primary_key=True)
    pfk_Num_Idf_Usr = db.Column(db.Integer, db.ForeignKey('Usr.Num_Idf_Usr'), primary_key=True)
    Nvl_Dif = db.Column(db.SmallInteger)  # Nível de dificuldade
    Qual = db.Column(db.SmallInteger)     # Qualidade
    Coment = db.Column(db.String(100))    # Comentário
