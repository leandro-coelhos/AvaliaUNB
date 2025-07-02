
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, TipoUsuario, Departamento, Disciplina, Professor, Turma, PeriodoLetivo
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Configuração do banco MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/avaliacao_professores'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o banco de dados
db.init_app(app)

@app.route('/')
def home():
    # Verificar se usuário está logado
    usuario_logado = None
    if 'user_id' in session:
        usuario_logado = Usuario.query.get(session['user_id'])
    
    return render_template('index.html', usuario=usuario_logado)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Buscar usuário no banco
        usuario = Usuario.query.filter_by(Email_Usr=email).first()
        
        if usuario and check_password_hash(usuario.Senha_Usr, senha):
            # Login bem-sucedido
            session['user_id'] = usuario.Num_Idf_Usr
            session['user_name'] = usuario.Nom_Usr
            session['user_type'] = usuario.fk_Cod_Tp_Usr
            
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos!', 'error')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        tipo_usuario = request.form.get('tipo_usuario')
        
        # Validações
        if senha != confirmar_senha:
            flash('As senhas não conferem!', 'error')
            return render_template('cadastro.html')
        
        if len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres!', 'error')
            return render_template('cadastro.html')
        
        # Verificar se o usuário já existe
        usuario_existente = Usuario.query.filter_by(Email_Usr=email).first()
        if usuario_existente:
            flash('Este email já está cadastrado!', 'error')
            return render_template('cadastro.html')
        
        # Hash da senha
        senha_hash = generate_password_hash(senha)
        
        # Criar novo usuário
        novo_usuario = Usuario(
            Nom_Usr=nome,
            Email_Usr=email,
            Tel_Usr=telefone,
            Mat_Usr=matricula,
            Senha_Usr=senha_hash,
            fk_Cod_Tp_Usr=int(tipo_usuario)
        )
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao realizar cadastro. Tente novamente.', 'error')
    
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/professores')
def listar_professores():
    # Verificar se usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página!', 'error')
        return redirect(url_for('login'))
    
    professores = Professor.query.all()
    return render_template('professores.html', professores=professores)

@app.route('/disciplinas')
def listar_disciplinas():
    # Verificar se usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página!', 'error')
        return redirect(url_for('login'))
    
    disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=disciplinas)

# Função auxiliar para verificar se usuário é admin
def is_admin():
    return session.get('user_type') == 2

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
