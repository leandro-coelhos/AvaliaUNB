
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Usuario, TipoUsuario, Departamento, Disciplina, Professor, Turma, PeriodoLetivo
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Configuração do banco MySQL
# Formato: mysql+pymysql://usuario:senha@host:porta/nome_banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/avaliacao_professores'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o banco de dados
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Aqui você implementaria a lógica de autenticação
        # Por enquanto, apenas uma validação básica
        usuario = Usuario.query.filter_by(Email_Usr=email).first()
        
        if usuario:
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário não encontrado!', 'error')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        matricula = request.form.get('matricula')
        tipo_usuario = request.form.get('tipo_usuario')
        
        # Verificar se o usuário já existe
        usuario_existente = Usuario.query.filter_by(Email_Usr=email).first()
        if usuario_existente:
            flash('Este email já está cadastrado!', 'error')
            return render_template('cadastro.html')
        
        # Criar novo usuário
        novo_usuario = Usuario(
            Nom_Usr=nome,
            Email_Usr=email,
            Tel_Usr=telefone,
            Mat_Usr=matricula,
            fk_Cod_Tp_Usr=int(tipo_usuario)
        )
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao realizar cadastro. Tente novamente.', 'error')
    
    return render_template('cadastro.html')

@app.route('/professores')
def listar_professores():
    professores = Professor.query.all()
    return render_template('professores.html', professores=professores)

@app.route('/disciplinas')
def listar_disciplinas():
    disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=disciplinas)

# Função para criar as tabelas no banco
def create_tables():
    with app.app_context():
        db.create_all()
        
        # Criar tipos de usuário padrão se não existirem
        if not TipoUsuario.query.first():
            tipo_aluno = TipoUsuario(Cod_Tp_Usr=1, Nom_Tp_Usr='Aluno')
            tipo_admin = TipoUsuario(Cod_Tp_Usr=2, Nom_Tp_Usr='Administrador')
            
            db.session.add(tipo_aluno)
            db.session.add(tipo_admin)
            db.session.commit()

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000, debug=True)
