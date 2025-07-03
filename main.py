
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import FormularioLogin, FormularioCadastro, FormularioFeedback
from models import db, Usuario, Professor, Turma, Feedback, Disciplina, TipoUsuario
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avaliacao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    formulario = FormularioLogin()
    if formulario.validate_on_submit():
        usuario = Usuario.query.filter_by(email_usuario=formulario.email.data).first()
        if usuario and check_password_hash(usuario.senha_usuario, formulario.senha.data):
            session['usuario_id'] = usuario.numero_identificacao_usuario
            session['nome_usuario'] = usuario.nome_usuario
            session['tipo_usuario'] = usuario.fk_codigo_tipo_usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos!', 'danger')
    return render_template('login.html', form=formulario)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    formulario = FormularioCadastro()
    if formulario.validate_on_submit():
        usuario_existente = Usuario.query.filter(
            (Usuario.email_usuario == formulario.email.data) |
            (Usuario.matricula_usuario == formulario.matricula.data)
        ).first()
        
        if usuario_existente:
            flash('Email ou matrícula já cadastrados!', 'danger')
        else:
            novo_usuario = Usuario(
                nome_usuario=formulario.nome.data,
                email_usuario=formulario.email.data,
                telefone_usuario=formulario.telefone.data,
                matricula_usuario=formulario.matricula.data,
                senha_usuario=generate_password_hash(formulario.senha.data),
                fk_codigo_tipo_usuario=formulario.tipo_usuario.data
            )
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
    return render_template('cadastro.html', form=formulario)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/professores')
def professores():
    try:
        resultado = db.session.execute(text("CALL ListarProfessoresComFeedbacks()"))
        professores_data = resultado.fetchall()
        return render_template('professores.html', professores=professores_data)
    except Exception as e:
        flash(f'Erro ao buscar professores: {str(e)}', 'danger')
        lista_professores = Professor.query.all()
        return render_template('professores.html', professores=lista_professores)

@app.route('/disciplinas')
def disciplinas():
    lista_disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=lista_disciplinas)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para dar feedback!', 'warning')
        return redirect(url_for('login'))
    
    formulario = FormularioFeedback()
    formulario.professor.choices = [(p.codigo_professor, p.nome_professor) for p in Professor.query.all()]
    formulario.turma.choices = [(t.numero_identificacao_turma, f"Turma {t.numero_identificacao_turma} - {t.disciplina.nome_disciplina}") for t in Turma.query.all()]
    
    if formulario.validate_on_submit():
        feedback_existente = Feedback.query.filter_by(
            pfk_numero_identificacao_turma=formulario.turma.data,
            pfk_codigo_professor=formulario.professor.data,
            pfk_numero_identificacao_usuario=session['usuario_id']
        ).first()
        
        if feedback_existente:
            flash('Você já avaliou este professor nesta turma!', 'warning')
        else:
            novo_feedback = Feedback(
                pfk_numero_identificacao_turma=formulario.turma.data,
                pfk_codigo_professor=formulario.professor.data,
                pfk_numero_identificacao_usuario=session['usuario_id'],
                nivel_dificuldade=formulario.dificuldade.data,
                qualidade=formulario.qualidade.data,
                comentario=formulario.comentario.data
            )
            db.session.add(novo_feedback)
            db.session.commit()
            flash('Feedback enviado com sucesso!', 'success')
            return redirect(url_for('home'))
    
    return render_template('feedback.html', form=formulario)

@app.route('/meus_feedbacks')
def meus_feedbacks():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado!', 'warning')
        return redirect(url_for('login'))
    
    feedbacks_usuario = Feedback.query.filter_by(pfk_numero_identificacao_usuario=session['usuario_id']).all()
    return render_template('meus_feedbacks.html', feedbacks=feedbacks_usuario)

@app.route('/feedback/editar/<int:turma_id>/<int:professor_id>', methods=['GET', 'POST'])
def editar_feedback(turma_id, professor_id):
    if 'usuario_id' not in session:
        flash('Você precisa estar logado!', 'warning')
        return redirect(url_for('login'))
    
    feedback = Feedback.query.filter_by(
        pfk_numero_identificacao_turma=turma_id,
        pfk_codigo_professor=professor_id,
        pfk_numero_identificacao_usuario=session['usuario_id']
    ).first_or_404()
    
    formulario = FormularioFeedback()
    formulario.professor.choices = [(p.codigo_professor, p.nome_professor) for p in Professor.query.all()]
    formulario.turma.choices = [(t.numero_identificacao_turma, f"Turma {t.numero_identificacao_turma} - {t.disciplina.nome_disciplina}") for t in Turma.query.all()]
    
    if formulario.validate_on_submit():
        feedback.nivel_dificuldade = formulario.dificuldade.data
        feedback.qualidade = formulario.qualidade.data
        feedback.comentario = formulario.comentario.data
        db.session.commit()
        flash('Feedback atualizado com sucesso!', 'success')
        return redirect(url_for('meus_feedbacks'))
    
    if request.method == 'GET':
        formulario.professor.data = feedback.pfk_codigo_professor
        formulario.turma.data = feedback.pfk_numero_identificacao_turma
        formulario.dificuldade.data = feedback.nivel_dificuldade
        formulario.qualidade.data = feedback.qualidade
        formulario.comentario.data = feedback.comentario
    
    return render_template('feedback.html', form=formulario, editing=True)

@app.route('/feedback/excluir/<int:turma_id>/<int:professor_id>', methods=['POST'])
def excluir_feedback(turma_id, professor_id):
    if 'usuario_id' not in session:
        flash('Você precisa estar logado!', 'warning')
        return redirect(url_for('login'))
    
    feedback = Feedback.query.filter_by(
        pfk_numero_identificacao_turma=turma_id,
        pfk_codigo_professor=professor_id,
        pfk_numero_identificacao_usuario=session['usuario_id']
    ).first_or_404()
    
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback excluído com sucesso!', 'success')
    return redirect(url_for('meus_feedbacks'))

@app.route('/professor/<int:professor_id>/feedbacks')
def feedbacks_detalhes(professor_id):
    professor = Professor.query.get_or_404(professor_id)
    
    try:
        resultado_feedbacks = db.session.execute(text("CALL BuscarFeedbacksProfessor(:prof_id)"), {"prof_id": professor_id})
        feedbacks_data = resultado_feedbacks.fetchall()
        
        resultado_medias = db.session.execute(text("CALL CalcularMediasProfessor(:prof_id)"), {"prof_id": professor_id})
        medias_data = resultado_medias.fetchone()
        
        if medias_data:
            media_qualidade = round(float(medias_data.media_qualidade), 1)
            media_dificuldade = round(float(medias_data.media_dificuldade), 1)
        else:
            media_qualidade = 0
            media_dificuldade = 0
        
        return render_template('feedbacks_detalhes.html', 
                             professor=professor, 
                             feedbacks=feedbacks_data,
                             media_qualidade=media_qualidade,
                             media_dificuldade=media_dificuldade)
    except Exception as e:
        flash(f'Erro ao buscar feedbacks: {str(e)}', 'danger')
        return redirect(url_for('professores'))

@app.route('/turmas_avaliadas')
def turmas_avaliadas():
    turmas_com_feedbacks = db.session.query(Turma).join(Feedback).distinct().all()
    return render_template('turmas_avaliadas.html', turmas=turmas_com_feedbacks)

@app.route('/turma/<int:turma_id>/feedbacks')
def feedbacks_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    
    try:
        resultado = db.session.execute(text("CALL BuscarFeedbacksPorTurma(:turma_id)"), {"turma_id": turma_id})
        feedbacks_data = resultado.fetchall()
        
        return render_template('feedbacks_turma.html', 
                             turma=turma, 
                             feedbacks=feedbacks_data)
    except Exception as e:
        flash(f'Erro ao buscar feedbacks da turma: {str(e)}', 'danger')
        return redirect(url_for('turmas_avaliadas'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
