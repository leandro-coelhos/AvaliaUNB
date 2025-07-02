from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, TipoUsuario, Departamento, Disciplina, Professor, Turma, PeriodoLetivo, Feedback
from forms import LoginForm, CadastroForm, FeedbackForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Configuração do banco PostgreSQL
import os
database_url = os.environ.get('DATABASE_URL', 'sqlite:///avaliacao_professores.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
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
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

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

    return render_template('login.html', form=form)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()

    if form.validate_on_submit():
        # Verificar se o usuário já existe
        usuario_existente = Usuario.query.filter_by(Email_Usr=form.email.data).first()
        if usuario_existente:
            flash('Este email já está cadastrado!', 'error')
            return render_template('cadastro.html', form=form)

        # Hash da senha
        senha_hash = generate_password_hash(form.senha.data)

        # Criar novo usuário
        novo_usuario = Usuario(
            Nom_Usr=form.nome.data,
            Email_Usr=form.email.data,
            Tel_Usr=form.telefone.data,
            Mat_Usr=form.matricula.data,
            Senha_Usr=senha_hash,
            fk_Cod_Tp_Usr=int(form.tipo_usuario.data)
        )

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao realizar cadastro. Tente novamente.', 'error')

    return render_template('cadastro.html', form=form)

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

@app.route('/feedback', methods=['GET', 'POST'])
def criar_feedback():
    # Verificar se usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página!', 'error')
        return redirect(url_for('login'))

    form = FeedbackForm()

    # Carregar opções dinamicamente
    professores = Professor.query.all()
    turmas = Turma.query.all()

    form.professor.choices = [(0, 'Selecione um professor')] + [(p.Cod_Prof, p.Nom_Prof) for p in professores]
    form.turma.choices = [(0, 'Selecione uma turma')] + [(t.Num_Idf_Tur, f"Turma {t.Num_Idf_Tur} - {t.disciplina.Nom_Dis}") for t in turmas]

    if form.validate_on_submit():
        # Verificar se o usuário já deu feedback para esta turma
        feedback_existente = Feedback.query.filter_by(
            pfk_Num_Idf_Tur=int(form.turma.data),
            pfk_Cod_Prof=int(form.professor.data),
            pfk_Num_Idf_Usr=session['user_id']
        ).first()

        if feedback_existente:
            flash('Você já enviou um feedback para esta turma com este professor!', 'error')
            return render_template('feedback.html', form=form)

        novo_feedback = Feedback(
            pfk_Num_Idf_Tur=int(form.turma.data),
            pfk_Cod_Prof=int(form.professor.data),
            pfk_Num_Idf_Usr=session['user_id'],
            Nvl_Dif=int(form.dificuldade.data),
            Qual=form.qualidade.data,
            Coment=form.comentario.data
        )

        try:
            db.session.add(novo_feedback)
            db.session.commit()
            flash('Feedback enviado com sucesso!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao enviar feedback. Tente novamente.', 'error')

    return render_template('feedback.html', form=form)

@app.route('/turmas-avaliadas')
def listar_turmas_avaliadas():
    # Verificar se usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página!', 'error')
        return redirect(url_for('login'))

    # Buscar todas as combinações únicas de turma/professor que têm feedbacks com médias
    turmas_professores = db.session.query(
        Feedback.pfk_Num_Idf_Tur,
        Feedback.pfk_Cod_Prof,
        Turma.Num_Idf_Tur,
        Professor.Nom_Prof,
        Disciplina.Nom_Dis,
        db.func.count(Feedback.pfk_Num_Idf_Usr).label('total_feedbacks'),
        db.func.avg(Feedback.Qual).label('media_qualidade'),
        db.func.avg(Feedback.Nvl_Dif).label('media_dificuldade')
    ).join(
        Turma, Feedback.pfk_Num_Idf_Tur == Turma.Num_Idf_Tur
    ).join(
        Professor, Feedback.pfk_Cod_Prof == Professor.Cod_Prof
    ).join(
        Disciplina, Turma.fk_Cod_Dis == Disciplina.Cod_Dis
    ).group_by(
        Feedback.pfk_Num_Idf_Tur, Feedback.pfk_Cod_Prof
    ).all()

    return render_template('turmas_avaliadas.html', turmas_professores=turmas_professores)

@app.route('/meus-feedbacks')
def meus_feedbacks():
    # Verificar se usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página!', 'error')
        return redirect(url_for('login'))

    # Buscar todos os feedbacks do usuário logado
    feedbacks_usuario = db.session.query(
        Feedback,
        Turma,
        Professor,
        Disciplina
    ).join(
        Turma, Feedback.pfk_Num_Idf_Tur == Turma.Num_Idf_Tur
    ).join(
        Professor, Feedback.pfk_Cod_Prof == Professor.Cod_Prof
    ).join(
        Disciplina, Turma.fk_Cod_Dis == Disciplina.Cod_Dis
    ).filter(
        Feedback.pfk_Num_Idf_Usr == session['user_id']
    ).all()

    return render_template('meus_feedbacks.html', feedbacks=feedbacks_usuario)

@app.route('/feedbacks/<int:turma_id>/<int:professor_id>')
def ver_feedbacks(turma_id, professor_id):
    # Verificar se usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página!', 'error')
        return redirect(url_for('login'))

    # Buscar informações da turma e professor
    turma = Turma.query.get_or_404(turma_id)
    professor = Professor.query.get_or_404(professor_id)

    # Buscar todos os feedbacks para essa combinação turma/professor
    feedbacks = Feedback.query.filter_by(
        pfk_Num_Idf_Tur=turma_id,
        pfk_Cod_Prof=professor_id
    ).join(Usuario).all()

    # Calcular estatísticas
    if feedbacks:
        media_dificuldade = sum(f.Nvl_Dif for f in feedbacks) / len(feedbacks)
        media_qualidade = sum(f.Qual for f in feedbacks) / len(feedbacks)
    else:
        media_dificuldade = 0
        media_qualidade = 0

    return render_template('feedbacks_detalhes.html', 
                         turma=turma, 
                         professor=professor, 
                         feedbacks=feedbacks,
                         media_dificuldade=round(media_dificuldade, 1),
                         media_qualidade=round(media_qualidade, 1),
                         total_feedbacks=len(feedbacks))

@app.route('/editar-feedback/<int:turma_id>/<int:professor_id>', methods=['GET', 'POST'])
def editar_feedback(turma_id, professor_id):
    # Verificar se usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página!', 'error')
        return redirect(url_for('login'))

    # Buscar o feedback do usuário
    feedback = Feedback.query.filter_by(
        pfk_Num_Idf_Tur=turma_id,
        pfk_Cod_Prof=professor_id,
        pfk_Num_Idf_Usr=session['user_id']
    ).first_or_404()

    # Buscar informações da turma e professor
    turma = Turma.query.get(turma_id)
    professor = Professor.query.get(professor_id)

    form = FeedbackForm()

    # Carregar opções dinamicamente
    professores = Professor.query.all()
    turmas = Turma.query.all()

    form.professor.choices = [(0, 'Selecione um professor')] + [(p.Cod_Prof, p.Nom_Prof) for p in professores]
    form.turma.choices = [(0, 'Selecione uma turma')] + [(t.Num_Idf_Tur, f"Turma {t.Num_Idf_Tur} - {t.disciplina.Nom_Dis}") for t in turmas]

    if request.method == 'GET':
        # Preencher formulário com dados existentes
        form.professor.data = str(feedback.pfk_Cod_Prof)
        form.turma.data = str(feedback.pfk_Num_Idf_Tur)
        form.dificuldade.data = feedback.Nvl_Dif
        form.qualidade.data = feedback.Qual
        form.comentario.data = feedback.Coment

    if form.validate_on_submit():
        # Verificar se mudou turma/professor e já existe feedback
        if (int(form.turma.data) != turma_id or int(form.professor.data) != professor_id):
            feedback_existente = Feedback.query.filter_by(
                pfk_Num_Idf_Tur=int(form.turma.data),
                pfk_Cod_Prof=int(form.professor.data),
                pfk_Num_Idf_Usr=session['user_id']
            ).first()

            if feedback_existente:
                flash('Você já tem um feedback para esta nova combinação de turma e professor!', 'error')
                return render_template('feedback.html', form=form, editing=True, turma=turma, professor=professor)

        # Atualizar feedback
        feedback.pfk_Num_Idf_Tur = int(form.turma.data)
        feedback.pfk_Cod_Prof = int(form.professor.data)
        feedback.Nvl_Dif = int(form.dificuldade.data)
        feedback.Qual = form.qualidade.data
        feedback.Coment = form.comentario.data

        try:
            db.session.commit()
            flash('Feedback atualizado com sucesso!', 'success')
            return redirect(url_for('meus_feedbacks'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar feedback. Tente novamente.', 'error')

    return render_template('feedback.html', form=form, editing=True, turma=turma, professor=professor)

@app.route('/excluir-feedback/<int:turma_id>/<int:professor_id>', methods=['POST'])
def excluir_feedback(turma_id, professor_id):
    # Verificar se usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar esta página!', 'error')
        return redirect(url_for('login'))

    # Buscar o feedback do usuário
    feedback = Feedback.query.filter_by(
        pfk_Num_Idf_Tur=turma_id,
        pfk_Cod_Prof=professor_id,
        pfk_Num_Idf_Usr=session['user_id']
    ).first_or_404()

    try:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir feedback. Tente novamente.', 'error')

    return redirect(url_for('meus_feedbacks'))

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