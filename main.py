from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
import io
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from forms import FormularioLogin, FormularioCadastro, FormularioFeedback, FormularioDisciplina, FormularioTipoUsuario, FormularioProfessor
from models import db, Usuario, Professor, Turma, Feedback, Disciplina, TipoUsuario, DocumentoAvaliacao, CriterioAvaliacaoTurma
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from procedures import ProceduresSimuladas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avaliacao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

    try:
        
        db.session.execute(text("""
        CREATE VIEW IF NOT EXISTS view_professores_com_feedbacks AS
        SELECT p.Cod_Prof as codigo_professor,
               p.Nom_Prof as nome_professor,
               COUNT(f.pfk_Cod_Prof) as total_feedbacks,
               COALESCE(AVG(f.Qual), 0) as media_qualidade,
               COALESCE(AVG(f.Nvl_Dif), 0) as media_dificuldade
        FROM Prof p
        LEFT JOIN Fdbk f ON p.Cod_Prof = f.pfk_Cod_Prof
        GROUP BY p.Cod_Prof, p.Nom_Prof
        ORDER BY p.Nom_Prof
        """))

        db.session.execute(text("""
        CREATE VIEW IF NOT EXISTS view_feedbacks_professor AS
        SELECT f.pfk_Num_Idf_Tur as turma_id,
               f.pfk_Cod_Prof as professor_id,
               f.pfk_Num_Idf_Usr as usuario_id,
               f.Nvl_Dif as nivel_dificuldade,
               f.Qual as qualidade,
               f.Coment as comentario,
               u.Nom_Usr as nome_usuario,
               t.Num_Idf_Tur as numero_turma,
               d.Nom_Dis as nome_disciplina,
               p.Nom_Prof as nome_professor,
               t.fk_Cod_Per as periodo_codigo,
               COALESCE(pl.Ano_Per, CAST(SUBSTR(t.fk_Cod_Per, 1, 4) AS INTEGER)) as ano_periodo,
               COALESCE(pl.Seq_Per, CAST(SUBSTR(t.fk_Cod_Per, 6, 1) AS INTEGER)) as sequencial_periodo
        FROM Fdbk f
        JOIN Usr u ON f.pfk_Num_Idf_Usr = u.Num_Idf_Usr
        JOIN Tur t ON f.pfk_Num_Idf_Tur = t.Num_Idf_Tur
        JOIN Dis d ON t.fk_Cod_Dis = d.Cod_Dis
        JOIN Prof p ON f.pfk_Cod_Prof = p.Cod_Prof
        LEFT JOIN Per_Let pl ON t.fk_Cod_Per = pl.Cod_Per
        """))

        db.session.execute(text("""
        CREATE VIEW IF NOT EXISTS view_medias_professor AS
        SELECT f.pfk_Cod_Prof as professor_id,
               p.Nom_Prof as nome_professor,
               AVG(f.Qual) as media_qualidade,
               AVG(f.Nvl_Dif) as media_dificuldade,
               COUNT(*) as total_feedbacks
        FROM Fdbk f
        JOIN Prof p ON f.pfk_Cod_Prof = p.Cod_Prof
        GROUP BY f.pfk_Cod_Prof, p.Nom_Prof
        """))

        db.session.execute(text("""
        CREATE VIEW IF NOT EXISTS view_feedbacks_turma AS
        SELECT f.pfk_Num_Idf_Tur as turma_id,
               f.pfk_Cod_Prof as professor_id,
               f.pfk_Num_Idf_Usr as usuario_id,
               f.Nvl_Dif as nivel_dificuldade,
               f.Qual as qualidade,
               f.Coment as comentario,
               u.Nom_Usr as nome_usuario,
               p.Nom_Prof as nome_professor,
               d.Nom_Dis as nome_disciplina,
               t.fk_Cod_Per as periodo_codigo,
               pl.Ano_Per as ano_periodo,
               pl.Seq_Per as sequencial_periodo
        FROM Fdbk f
        JOIN Usr u ON f.pfk_Num_Idf_Usr = u.Num_Idf_Usr
        JOIN Prof p ON f.pfk_Cod_Prof = p.Cod_Prof
        JOIN Tur t ON f.pfk_Num_Idf_Tur = t.Num_Idf_Tur
        JOIN Dis d ON t.fk_Cod_Dis = d.Cod_Dis
        LEFT JOIN Per_Let pl ON t.fk_Cod_Per = pl.Cod_Per
        """))

        db.session.commit()
        print("Views criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar views: {e}")
        db.session.rollback()

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
            
            if usuario.fk_codigo_tipo_usuario == 3:  
                return redirect(url_for('meus_reviews'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos!', 'danger')
    return render_template('login.html', form=formulario)

@app.route('/tipo_usuario', methods=['GET', 'POST'])
def tipo_usuario():
    from forms import FormularioTipoUsuario
    formulario_tipo = FormularioTipoUsuario()

    if formulario_tipo.validate_on_submit():
        session['tipo_usuario_selecionado'] = formulario_tipo.tipo_usuario.data
        if formulario_tipo.tipo_usuario.data == 3:
            return redirect(url_for('cadastro_professor'))
        else:
            return redirect(url_for('cadastro', tipo=formulario_tipo.tipo_usuario.data))

    return render_template('selecao_tipo_usuario.html', form=formulario_tipo)


@app.route('/cadastro_professor', methods=['GET', 'POST'])
def cadastro_professor():
    formulario = FormularioProfessor()
    if formulario.validate_on_submit():
        try:
            usuario_existente = Usuario.query.filter(
                (Usuario.email_usuario == formulario.email.data) |
                (Usuario.matricula_usuario == str(formulario.professor_existente.data))
            ).first()

            if usuario_existente:
                flash('Email ou matrícula já cadastrados!', 'danger')
                return render_template('cadastro.html', form=formulario, tipo_usuario=3)
            # Verificar se o professor já existe
            professor_existente = Professor.query.filter_by(codigo_professor=formulario.codigo_professor.data).first()
            if professor_existente:
                flash('Professor já cadastrado!', 'danger')
                return render_template('cadastro.html', form=formulario, tipo_usuario=3)

            user = Usuario(
                nome_usuario=formulario.nome.data,
                email_usuario=formulario.email.data,
                telefone_usuario=formulario.telefone.data,
                matricula_usuario=str(formulario.professor_existente.data),
                senha_usuario=generate_password_hash(formulario.senha.data),
                fk_codigo_tipo_usuario=3  
            )


            db.session.add(user)
            db.session.commit()

            flash('Cadastro de professor realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar professor: {str(e)}', 'danger')

    return render_template('cadastro.html', form=formulario, tipo_usuario=3)

@app.route('/cadastro/<int:tipo>/', methods=['GET', 'POST'])
def cadastro(tipo):
    print(tipo)
    # Verificar se o tipo de usuário foi selecionado
    if 'tipo_usuario_selecionado' not in session:
        return redirect(url_for('tipo_usuario'))
    
    tipo_usuario = session['tipo_usuario_selecionado']
    
    # Criar o formulário com o tipo de usuário
    formulario = FormularioCadastro(tipo_usuario=tipo_usuario)

    print('Método:', request.method)
    print('Tipo de usuário:', tipo_usuario)
    print('Form enviado?', formulario.is_submitted())
    print('Form válido?', formulario.validate())
    print('Erros:', formulario.errors)

    if formulario.validate_on_submit():
        print('Formulário de cadastro enviado')
        try:
            # Lógica específica para professores
            if tipo_usuario == 3:
                if not formulario.professor_existente.data:
                    flash('Selecione seu perfil de professor!', 'danger')
                    return render_template('cadastro.html', form=formulario, tipo_usuario=tipo)
                matricula = str(formulario.professor_existente.data)
            else:
                matricula = formulario.matricula.data

            # Verificar se usuário já existe
            usuario_existente = Usuario.query.filter(
                (Usuario.email_usuario == formulario.email.data) |
                (Usuario.matricula_usuario == matricula)
            ).first()

            if usuario_existente:
                flash('Email ou matrícula já cadastrados!', 'danger')
                return render_template('cadastro.html', form=formulario, tipo_usuario=tipo_usuario)
            else:
                novo_usuario = Usuario(
                    nome_usuario=formulario.nome.data,
                    email_usuario=formulario.email.data,
                    telefone_usuario=formulario.telefone.data,
                    matricula_usuario=matricula,
                    senha_usuario=generate_password_hash(formulario.senha.data),
                    fk_codigo_tipo_usuario=tipo
                )
                db.session.add(novo_usuario)
                db.session.commit()

                # Limpar sessão
                session.pop('tipo_usuario_selecionado', None)

                flash('Cadastro realizado com sucesso! Faça login para acessar sua área.', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao realizar cadastro: {str(e)}', 'danger')
            return render_template('cadastro.html', form=formulario, tipo_usuario=tipo_usuario)

    return render_template('cadastro.html', form=formulario, tipo_usuario=tipo_usuario)

@app.route('/cadastro/reset')
def reset_cadastro():
    session.pop('tipo_usuario_selecionado', None)
    return redirect(url_for('cadastro'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/disciplinas')
def disciplinas():
    lista_disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=lista_disciplinas)

@app.route('/disciplina/<codigo_disciplina>/professores')
def professores_por_disciplina(codigo_disciplina):
    disciplina = Disciplina.query.get_or_404(codigo_disciplina)

    # Usar procedure simulada para buscar ranking de professores por disciplina
    try:
        professores_data = ProceduresSimuladas.obter_ranking_professores(codigo_disciplina)
        return render_template('professores_disciplina.html', 
                             professores=professores_data, 
                             disciplina=disciplina)
    except Exception as e:
        flash(f'Erro ao buscar professores da disciplina: {str(e)}', 'danger')
        return redirect(url_for('disciplinas'))

@app.route('/disciplinas/new', methods=['GET', 'POST'])
def create_disciplina():
    if 'usuario_id' not in session or session['tipo_usuario'] != 2:  # Apenas administradores
        flash('Você precisa estar logado como administrador para criar disciplinas!', 'warning')
        return redirect(url_for('login'))

    formulario = FormularioDisciplina()

    if formulario.validate_on_submit():
        nova_disciplina = Disciplina(
            codigo_disciplina=formulario.codigo_disciplina.data,
            nome_disciplina=formulario.nome_disciplina.data,
            fk_codigo_departamento=formulario.departamento.data
        )
        db.session.add(nova_disciplina)
        db.session.commit()
        flash('Disciplina criada com sucesso!', 'success')
        return redirect(url_for('disciplinas'))

    return render_template('new_disciplina.html', form=formulario)

@app.route('/api/turmas_por_periodo/<int:periodo_id>')
def turmas_por_periodo(periodo_id):
    """Retorna as turmas de um período específico"""
    try:
        from models import Turma, Disciplina, PeriodoLetivo
        
        # Buscar o período pelo ID para obter o código correto
        periodo = PeriodoLetivo.query.get(periodo_id)
        if not periodo:
            return jsonify({"error": "Período não encontrado"}), 404
        
        # Formar o código do período no formato "ano.semestre"
        periodo_codigo = f"{periodo.ano_periodo}.{periodo.sequencial_periodo}"
        
        turmas = db.session.query(Turma, Disciplina).join(
            Disciplina, Turma.fk_codigo_disciplina == Disciplina.codigo_disciplina
        ).filter(Turma.fk_codigo_periodo == periodo_codigo).all()
        
        turmas_data = [
            {
                "id": turma.numero_identificacao_turma,
                "nome": f"Turma {turma.numero_identificacao_turma} - {disciplina.nome_disciplina}"
            }
            for turma, disciplina in turmas
        ]
        
        return jsonify({"turmas": turmas_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/turmas_por_periodo_disciplina/<int:periodo_id>/<string:disciplina_codigo>')
def turmas_por_periodo_disciplina(periodo_id, disciplina_codigo):
    """Retorna ou cria turmas de uma disciplina em um período específico"""
    try:
        from models import Turma, Disciplina, PeriodoLetivo
        
        # Buscar o período pelo ID para obter o código correto
        periodo = PeriodoLetivo.query.get(periodo_id)
        if not periodo:
            return jsonify({"error": "Período não encontrado"}), 404
        
        # Formar o código do período no formato "ano.semestre"
        periodo_codigo = f"{periodo.ano_periodo}.{periodo.sequencial_periodo}"
        
        # Verificar se a disciplina existe
        disciplina = Disciplina.query.get(disciplina_codigo)
        if not disciplina:
            return jsonify({"error": "Disciplina não encontrada"}), 404
        
        # Buscar turmas existentes da disciplina no período
        turmas_existentes = Turma.query.filter_by(
            fk_codigo_disciplina=disciplina_codigo,
            fk_codigo_periodo=periodo_codigo
        ).all()
        
        # Se não houver turmas, criar uma nova
        if not turmas_existentes:
            # Buscar o próximo número de turma disponível
            ultimo_numero = db.session.query(db.func.max(Turma.numero_identificacao_turma)).scalar() or 0
            
            # Tentar encontrar um professor comum para essa disciplina
            professor_comum = db.session.execute(text("""
            SELECT p.Cod_Prof
            FROM Prof p
            JOIN Fdbk f ON p.Cod_Prof = f.pfk_Cod_Prof
            JOIN Tur t ON f.pfk_Num_Idf_Tur = t.Num_Idf_Tur
            WHERE t.fk_Cod_Dis = :disciplina_codigo
            GROUP BY p.Cod_Prof
            ORDER BY COUNT(*) DESC
            LIMIT 1
            """), {"disciplina_codigo": disciplina_codigo}).fetchone()
            
            professor_codigo = professor_comum.Cod_Prof if professor_comum else None
            
            nova_turma = Turma(
                numero_identificacao_turma=ultimo_numero + 1,
                fk_codigo_disciplina=disciplina_codigo,
                fk_codigo_periodo=periodo_codigo,
                professor_codigo=professor_codigo
            )
            db.session.add(nova_turma)
            db.session.commit()
            turmas_existentes = [nova_turma]
        
        turmas_data = [
            {
                "id": turma.numero_identificacao_turma,
                "nome": f"Turma {turma.numero_identificacao_turma} - {disciplina.nome_disciplina}"
            }
            for turma in turmas_existentes
        ]
        
        return jsonify({"turmas": turmas_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/professores_por_turma/<int:turma_id>')
def professores_por_turma(turma_id):
    """Retorna os professores que já deram aula na disciplina da turma específica"""
    try:
        # Buscar a turma para obter a disciplina
        turma = Turma.query.get(turma_id)
        if not turma:
            return jsonify({"error": "Turma não encontrada"}), 404
        
        # Buscar todos os professores que já deram aula nesta disciplina
        resultado = db.session.execute(text("""
        SELECT DISTINCT p.Cod_Prof as codigo_professor,
               p.Nom_Prof as nome_professor
        FROM Prof p
        JOIN Fdbk f ON p.Cod_Prof = f.pfk_Cod_Prof
        JOIN Tur t ON f.pfk_Num_Idf_Tur = t.Num_Idf_Tur
        WHERE t.fk_Cod_Dis = :disciplina_codigo
        ORDER BY p.Nom_Prof
        """), {"disciplina_codigo": turma.fk_codigo_disciplina})
        
        professores_disciplina = resultado.fetchall()
        
        professores_data = [
            {
                "codigo": professor.codigo_professor,
                "nome": professor.nome_professor
            }
            for professor in professores_disciplina
        ]
        
        # Se não houver professores que já deram aula nesta disciplina, 
        # retornar todos os professores como fallback
        if not professores_data:
            professores = db.session.execute(text("""
            SELECT p.Cod_Prof as codigo_professor,
                   p.Nom_Prof as nome_professor
            FROM Prof p
            ORDER BY p.Nom_Prof
            """)).fetchall()
            
            professores_data = [
                {"codigo": professor.codigo_professor, "nome": professor.nome_professor}
                for professor in professores
            ]
        
        return jsonify({"professores": professores_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para dar feedback!', 'warning')
        return redirect(url_for('login'))
    
    # Impedir que professores criem feedbacks
    if session.get('tipo_usuario') == 3:  # 3 = Professor
        flash('Professores não podem criar feedbacks. Acesse sua página de reviews para ver as avaliações recebidas.', 'warning')
        return redirect(url_for('meus_reviews'))

    formulario = FormularioFeedback()

    if formulario.validate_on_submit():
        # Validar se todos os campos obrigatórios estão preenchidos
        if not formulario.periodo.data or not formulario.disciplina.data or not formulario.turma.data or not formulario.professor.data:
            flash('Preencha todos os campos obrigatórios!', 'danger')
            return render_template('feedback.html', form=formulario)
            
        feedback_existente = Feedback.query.filter_by(
            pfk_numero_identificacao_turma=formulario.turma.data,
            pfk_codigo_professor=formulario.professor.data,
            pfk_numero_identificacao_usuario=session['usuario_id']
        ).first()

        if feedback_existente:
            flash('Você já avaliou este professor nesta turma!', 'warning')
        else:
            try:
                novo_feedback = Feedback(
                    pfk_numero_identificacao_turma=formulario.turma.data,
                    pfk_codigo_professor=formulario.professor.data,
                    pfk_numero_identificacao_usuario=session['usuario_id'],
                    nivel_dificuldade=formulario.dificuldade.data,
                    qualidade=formulario.qualidade.data,
                    comentario=formulario.comentario.data
                )
                db.session.add(novo_feedback)
                db.session.flush()

                # Processar documento se fornecido
                if formulario.arquivo_pdf.data and formulario.tipo_avaliacao.data:
                    criterio = CriterioAvaliacaoTurma.query.filter_by(
                        fk_numero_identificacao_turma=formulario.turma.data
                    ).first()

                    if not criterio:
                        criterio = CriterioAvaliacaoTurma(
                            fk_numero_identificacao_turma=formulario.turma.data,
                            fk_codigo_tipo_avaliacao=formulario.tipo_avaliacao.data
                        )
                        db.session.add(criterio)
                        db.session.flush()

                    arquivo = formulario.arquivo_pdf.data
                    documento = DocumentoAvaliacao(
                        nome_arquivo=arquivo.filename,
                        tipo_documento=str(formulario.tipo_avaliacao.data),
                        arquivo_documento=arquivo.read(),
                        fk_numero_identificacao_avaliacao=criterio.numero_identificacao_avaliacao,
                        fk_usuario_id=session['usuario_id'],
                        fk_professor_id=formulario.professor.data,
                        fk_turma_id=formulario.turma.data
                    )
                    db.session.add(documento)

                db.session.commit()
                flash('Feedback enviado com sucesso!', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao enviar feedback: {str(e)}', 'danger')

    return render_template('feedback.html', form=formulario)

@app.route('/meus_feedbacks')
def meus_feedbacks():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado!', 'warning')
        return redirect(url_for('login'))

    # Buscar feedbacks com joins para ter acesso aos dados relacionados incluindo período
    from models import PeriodoLetivo
    feedbacks_data = db.session.query(
        Feedback, Turma, Professor, Disciplina, PeriodoLetivo
    ).join(
        Turma, Feedback.pfk_numero_identificacao_turma == Turma.numero_identificacao_turma
    ).join(
        Professor, Feedback.pfk_codigo_professor == Professor.codigo_professor
    ).join(
        Disciplina, Turma.fk_codigo_disciplina == Disciplina.codigo_disciplina
    ).outerjoin(
        PeriodoLetivo, Turma.fk_codigo_periodo == PeriodoLetivo.codigo_periodo
    ).filter(
        Feedback.pfk_numero_identificacao_usuario == session['usuario_id']
    ).all()

    return render_template('meus_feedbacks.html', feedbacks=feedbacks_data)

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
    formulario.turma.choices = []  # Será preenchido dinamicamente

    if formulario.validate_on_submit():
        feedback.nivel_dificuldade = formulario.dificuldade.data
        feedback.qualidade = formulario.qualidade.data
        feedback.comentario = formulario.comentario.data

        if formulario.arquivo_pdf.data and formulario.tipo_avaliacao.data:
            criterio = CriterioAvaliacaoTurma.query.filter_by(
                fk_numero_identificacao_turma=turma_id
            ).first()

            if criterio:
                DocumentoAvaliacao.query.filter_by(
                    fk_numero_identificacao_avaliacao=criterio.numero_identificacao_avaliacao
                ).delete()

            arquivo = formulario.arquivo_pdf.data
            documento = DocumentoAvaliacao(
                nome_arquivo=arquivo.filename,
                tipo_documento=formulario.tipo_avaliacao.data,
                arquivo_documento=arquivo.read(),
                fk_numero_identificacao_avaliacao=criterio.numero_identificacao_avaliacao,
                fk_usuario_id=session['usuario_id'],
                fk_professor_id=professor_id,
                fk_turma_id=turma_id
            )
            db.session.add(documento)

        db.session.commit()
        flash('Feedback atualizado com sucesso!', 'success')
        return redirect(url_for('meus_feedbacks'))

    if request.method == 'GET':
        # Buscar o período e disciplina da turma
        turma = Turma.query.get(feedback.pfk_numero_identificacao_turma)
        if turma:
            formulario.periodo.data = turma.fk_codigo_periodo
            formulario.disciplina.data = turma.fk_codigo_disciplina
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

    if feedback:
        documentos = DocumentoAvaliacao.query.filter_by(
            fk_numero_identificacao_avaliacao=feedback.pfk_numero_identificacao_turma,
            fk_professor_id=professor_id,
            fk_usuario_id=session['usuario_id']
        ).all()
        for documento in documentos:
            db.session.delete(documento)
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback excluído com sucesso!', 'success')
    return redirect(url_for('meus_feedbacks'))

@app.route('/professor/<int:professor_id>/feedbacks')
def feedbacks_detalhes(professor_id):
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para ver os feedbacks!', 'warning')
        return redirect(url_for('login'))
    
    try:
        # Usar procedure simulada para buscar feedbacks
        feedbacks_data = ProceduresSimuladas.buscar_feedbacks_professor(professor_id)

        # Buscar documentos para cada feedback específico do usuário
        feedbacks_com_documentos = []
        for feedback in feedbacks_data:
            documentos_resultado = db.session.execute(text("""
            SELECT da.Num_Idf_Doc as numero_identificacao_documento,
                   da.Nome_Arq as nome_arquivo,
                   da.Tipo_Doc as tipo_documento
            FROM Doc_Aval da
            WHERE da.fk_Usr_Id = :usuario_id
            AND da.fk_Prof_Id = :professor_id
            AND da.fk_Tur_Id = :turma_id
            """), {
                "turma_id": feedback.turma_id,
                "usuario_id": feedback.usuario_id,
                "professor_id": feedback.professor_id
            })
            documentos = documentos_resultado.fetchall()
            
            feedback_dict = {
                'turma_id': feedback.turma_id,
                'professor_id': feedback.professor_id,
                'usuario_id': feedback.usuario_id,
                'nivel_dificuldade': feedback.nivel_dificuldade,
                'qualidade': feedback.qualidade,
                'comentario': feedback.comentario,
                'nome_usuario': feedback.nome_usuario,
                'numero_turma': feedback.numero_turma,
                'nome_disciplina': feedback.nome_disciplina,
                'disciplina_codigo': feedback.disciplina_codigo,
                'nome_professor': feedback.nome_professor,
                'periodo_codigo': feedback.periodo_codigo,
                'ano_periodo': feedback.ano_periodo if hasattr(feedback, 'ano_periodo') else None,
                'sequencial_periodo': feedback.sequencial_periodo if hasattr(feedback, 'sequencial_periodo') else None,
                'documentos': documentos
            }
            feedbacks_com_documentos.append(feedback_dict)

        if feedbacks_com_documentos:
            professor_nome = feedbacks_com_documentos[0]['nome_professor']
            disciplina_codigo = feedbacks_com_documentos[0]['disciplina_codigo']
            
            # Calcular estatísticas
            total_feedbacks = len(feedbacks_com_documentos)
            media_qualidade = sum(feedback['qualidade'] for feedback in feedbacks_com_documentos) / total_feedbacks
            media_dificuldade = sum(feedback['nivel_dificuldade'] for feedback in feedbacks_com_documentos) / total_feedbacks
        else:
            professor = Professor.query.get_or_404(professor_id)
            professor_nome = professor.nome_professor
            disciplina_codigo = 'CIC0004'  # fallback
            total_feedbacks = 0
            media_qualidade = 0
            media_dificuldade = 0

        return render_template('feedbacks_detalhes.html', 
                             feedbacks=feedbacks_com_documentos, 
                             professor_nome=professor_nome,
                             professor_id=professor_id,
                             disciplina_codigo=disciplina_codigo,
                             total_feedbacks=total_feedbacks,
                             media_qualidade=round(media_qualidade, 1),
                             media_dificuldade=round(media_dificuldade, 1))
    except Exception as e:
        flash(f'Erro ao buscar feedbacks: {str(e)}', 'danger')
        return redirect(url_for('disciplinas'))

@app.route('/turma/<int:turma_id>/feedbacks')
def feedbacks_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)

    try:
        resultado = db.session.execute(text("SELECT * FROM view_feedbacks_turma WHERE turma_id = :turma_id"), {"turma_id": turma_id})
        feedbacks_data = resultado.fetchall()

        return render_template('feedbacks_turma.html', 
                             turma=turma, 
                             feedbacks=feedbacks_data)
    except Exception as e:
        flash(f'Erro ao buscar feedbacks da turma: {str(e)}', 'danger')
        return redirect(url_for('turmas_avaliadas'))

@app.route('/turma/<int:turma_id>/documentos')
def documentos_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)

    # Buscar documentos relacionados à turma
    documentos = db.session.query(DocumentoAvaliacao).join(
        CriterioAvaliacaoTurma,
        DocumentoAvaliacao.fk_numero_identificacao_avaliacao == CriterioAvaliacaoTurma.numero_identificacao_avaliacao
    ).filter(
        CriterioAvaliacaoTurma.fk_numero_identificacao_turma == turma_id
    ).all()

    return render_template('documentos_turma.html', turma=turma, documentos=documentos)

@app.route('/documento/<int:documento_id>')
def baixar_documento(documento_id):
    documento = DocumentoAvaliacao.query.get_or_404(documento_id)
    return send_file(
        io.BytesIO(documento.arquivo_documento),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=documento.nome_arquivo
    )

@app.route('/professor/<int:professor_id>/documentos')
def documentos_professor(professor_id):
    try:
        professor = Professor.query.get_or_404(professor_id)

        resultado = db.session.execute(text("""
        SELECT da.Num_Idf_Doc as numero_identificacao_documento,
               da.Nome_Arq as nome_arquivo,
               da.Tipo_Doc as tipo_documento,
               d.Cod_Dis as disciplina_codigo
        FROM Doc_Aval da
        JOIN Crit_Aval_Tur cat ON da.fk_Num_Idf_Aval = cat.Num_Idf_Aval
        JOIN Tur t ON cat.fk_Num_Idf_Tur = t.Num_Idf_Tur
        JOIN Dis d ON t.fk_Cod_Dis = d.Cod_Dis
        JOIN Fdbk f ON t.Num_Idf_Tur = f.pfk_Num_Idf_Tur AND f.pfk_Cod_Prof = :prof_id
        ORDER BY da.Nome_Arq
        """), {"prof_id": professor_id})
        documentos_data = resultado.fetchall()

        # Pegar o código da disciplina do primeiro documento, ou usar um padrão
        disciplina_codigo = 'CIC0004'  # fallback
        if documentos_data:
            disciplina_codigo = documentos_data[0].disciplina_codigo

        return render_template('documentos_professor.html', 
                             documentos=documentos_data, 
                             professor=professor,
                             disciplina_codigo=disciplina_codigo)
    except Exception as e:
        flash(f'Erro ao buscar documentos: {str(e)}', 'danger')
        return redirect(url_for('home'))

@app.route('/estatisticas')
def estatisticas():
    """Página de estatísticas usando procedures simuladas"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    try:
        # Usar procedures simuladas
        stats_sistema = ProceduresSimuladas.obter_estatisticas_sistema()
        ranking_professores = ProceduresSimuladas.obter_ranking_professores()
        
        return render_template('estatisticas.html', 
                             stats=stats_sistema,
                             ranking=ranking_professores)
    except Exception as e:
        flash(f'Erro ao carregar estatísticas: {str(e)}', 'danger')
        return redirect(url_for('home'))

# ========== ROTAS ADMINISTRATIVAS ==========

@app.route('/admin/professores')
def admin_professores():
    """Página de gerenciamento de professores"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    professores = Professor.query.order_by(Professor.nome_professor).all()
    return render_template('admin_professores.html', professores=professores)

@app.route('/admin/professores/novo', methods=['GET', 'POST'])
def admin_novo_professor():
    """Criar novo professor"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    from forms import FormularioProfessorNovo
    formulario = FormularioProfessorNovo()
    
    if formulario.validate_on_submit():
        novo_professor = Professor(
            codigo_professor=formulario.codigo_professor.data,
            nome_professor=formulario.nome_professor.data
        )
        db.session.add(novo_professor)
        db.session.commit()
        flash('Professor criado com sucesso!', 'success')
        return redirect(url_for('admin_professores'))
    
    return render_template('admin_form_professor.html', form=formulario, titulo='Novo Professor')

@app.route('/admin/professores/<int:codigo_professor>/editar', methods=['GET', 'POST'])
def admin_editar_professor(codigo_professor):
    """Editar professor existente"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    professor = Professor.query.get_or_404(codigo_professor)
    from forms import FormularioProfessorNovo
    formulario = FormularioProfessorNovo(obj=professor)
    
    if formulario.validate_on_submit():
        professor.nome_professor = formulario.nome_professor.data
        db.session.commit()
        flash('Professor atualizado com sucesso!', 'success')
        return redirect(url_for('admin_professores'))
    
    return render_template('admin_form_professor.html', form=formulario, titulo='Editar Professor', professor=professor)

@app.route('/admin/professores/<int:codigo_professor>/excluir', methods=['POST'])
def admin_excluir_professor(codigo_professor):
    """Excluir professor"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    professor = Professor.query.get_or_404(codigo_professor)
    
    # Verificar se professor tem feedbacks
    feedbacks = Feedback.query.filter_by(pfk_codigo_professor=codigo_professor).first()
    if feedbacks:
        flash('Não é possível excluir professor que possui feedbacks!', 'danger')
        return redirect(url_for('admin_professores'))
    
    db.session.delete(professor)
    db.session.commit()
    flash('Professor excluído com sucesso!', 'success')
    return redirect(url_for('admin_professores'))

@app.route('/admin/disciplinas')
def admin_disciplinas():
    """Página de gerenciamento de disciplinas"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    disciplinas = Disciplina.query.order_by(Disciplina.nome_disciplina).all()
    return render_template('admin_disciplinas.html', disciplinas=disciplinas)

@app.route('/admin/disciplinas/nova', methods=['GET', 'POST'])
def admin_nova_disciplina():
    """Criar nova disciplina"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    formulario = FormularioDisciplina()
    
    if formulario.validate_on_submit():
        nova_disciplina = Disciplina(
            codigo_disciplina=formulario.codigo_disciplina.data,
            nome_disciplina=formulario.nome_disciplina.data,
            fk_codigo_departamento=formulario.departamento.data
        )
        db.session.add(nova_disciplina)
        db.session.commit()
        flash('Disciplina criada com sucesso!', 'success')
        return redirect(url_for('admin_disciplinas'))
    
    return render_template('new_disciplina.html', form=formulario, titulo='Nova Disciplina')

@app.route('/admin/disciplinas/<string:codigo_disciplina>/editar', methods=['GET', 'POST'])
def admin_editar_disciplina(codigo_disciplina):
    """Editar disciplina existente"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    disciplina = Disciplina.query.get_or_404(codigo_disciplina)
    formulario = FormularioDisciplina(obj=disciplina)
    
    if formulario.validate_on_submit():
        disciplina.nome_disciplina = formulario.nome_disciplina.data
        disciplina.fk_codigo_departamento = formulario.departamento.data
        db.session.commit()
        flash('Disciplina atualizada com sucesso!', 'success')
        return redirect(url_for('admin_disciplinas'))
    
    return render_template('new_disciplina.html', form=formulario, titulo='Editar Disciplina', disciplina=disciplina)

@app.route('/admin/disciplinas/<string:codigo_disciplina>/excluir', methods=['POST'])
def admin_excluir_disciplina(codigo_disciplina):
    """Excluir disciplina"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    disciplina = Disciplina.query.get_or_404(codigo_disciplina)
    
    # Verificar se disciplina tem turmas
    turmas = Turma.query.filter_by(fk_codigo_disciplina=codigo_disciplina).first()
    if turmas:
        flash('Não é possível excluir disciplina que possui turmas!', 'danger')
        return redirect(url_for('admin_disciplinas'))
    
    db.session.delete(disciplina)
    db.session.commit()
    flash('Disciplina excluída com sucesso!', 'success')
    return redirect(url_for('admin_disciplinas'))

@app.route('/admin/turmas')
def admin_turmas():
    """Página de gerenciamento de turmas"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    # Buscar todas as turmas com informações de professores
    turmas_query = db.session.query(
        Turma.numero_identificacao_turma,
        Turma.fk_codigo_disciplina,
        Turma.fk_codigo_periodo,
        Turma.professor_codigo,
        Disciplina.nome_disciplina,
        Professor.codigo_professor,
        Professor.nome_professor,
        db.func.count(Feedback.pfk_numero_identificacao_usuario).label('total_feedbacks_recebidos')
    ).join(
        Disciplina, Turma.fk_codigo_disciplina == Disciplina.codigo_disciplina
    ).outerjoin(
        Professor, Turma.professor_codigo == Professor.codigo_professor
    ).outerjoin(
        Feedback, Turma.numero_identificacao_turma == Feedback.pfk_numero_identificacao_turma
    ).group_by(
        Turma.numero_identificacao_turma,
        Turma.fk_codigo_disciplina,
        Turma.fk_codigo_periodo,
        Turma.professor_codigo,
        Disciplina.nome_disciplina,
        Professor.codigo_professor,
        Professor.nome_professor
    ).order_by(Turma.numero_identificacao_turma)
    
    turmas_data = turmas_query.all()
    
    return render_template('admin_turmas.html', turmas=turmas_data)

@app.route('/admin/turmas/nova', methods=['GET', 'POST'])
def admin_nova_turma():
    """Criar nova turma"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    from forms import FormularioTurma
    formulario = FormularioTurma()
    
    if formulario.validate_on_submit():
        try:
            # Verificar se o número da turma já existe
            numero_turma = formulario.numero_identificacao_turma.data
            turma_existente = Turma.query.get(numero_turma)
            
            if turma_existente:
                flash(f'Já existe uma turma com o número {numero_turma}!', 'danger')
                return render_template('admin_form_turma.html', form=formulario, titulo='Nova Turma')
            
            nova_turma = Turma(
                numero_identificacao_turma=numero_turma,
                fk_codigo_disciplina=formulario.disciplina.data,
                fk_codigo_periodo=formulario.periodo.data,
                professor_codigo=formulario.professor.data if formulario.professor.data and formulario.professor.data > 0 else None
            )
            db.session.add(nova_turma)
            
            db.session.commit()
            flash('Turma criada com sucesso!', 'success')
            return redirect(url_for('admin_turmas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar turma: {str(e)}', 'danger')
            return render_template('admin_form_turma.html', form=formulario, titulo='Nova Turma')
    
    return render_template('admin_form_turma.html', form=formulario, titulo='Nova Turma')

@app.route('/admin/turmas/<int:numero_turma>/editar', methods=['GET', 'POST'])
def admin_editar_turma(numero_turma):
    """Editar turma existente"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    turma = Turma.query.get_or_404(numero_turma)
    from forms import FormularioTurma
    formulario = FormularioTurma(obj=turma)
    
    # Preencher dados atuais da turma no formulário
    if formulario.professor.data == 0 and turma.professor_codigo:
        formulario.professor.data = turma.professor_codigo
    
    if formulario.validate_on_submit():
        turma.fk_codigo_disciplina = formulario.disciplina.data
        turma.fk_codigo_periodo = formulario.periodo.data
        turma.professor_codigo = formulario.professor.data if formulario.professor.data and formulario.professor.data > 0 else None
        
        db.session.commit()
        flash('Turma atualizada com sucesso!', 'success')
        return redirect(url_for('admin_turmas'))
    
    return render_template('admin_form_turma.html', form=formulario, titulo='Editar Turma', turma=turma)

@app.route('/admin/turmas/<int:numero_turma>/excluir', methods=['POST'])
def admin_excluir_turma(numero_turma):
    """Excluir turma"""
    if 'usuario_id' not in session or session.get('tipo_usuario') != 2:
        flash('Acesso restrito a administradores!', 'warning')
        return redirect(url_for('home'))
    
    turma = Turma.query.get_or_404(numero_turma)
    
    # Verificar se turma tem feedbacks
    feedbacks = Feedback.query.filter_by(pfk_numero_identificacao_turma=numero_turma).first()
    if feedbacks:
        flash('Não é possível excluir turma que possui feedbacks!', 'danger')
        return redirect(url_for('admin_turmas'))
    
    db.session.delete(turma)
    db.session.commit()
    flash('Turma excluída com sucesso!', 'success')
    return redirect(url_for('admin_turmas'))

@app.route('/meus_reviews')
def meus_reviews():
    """Página para professores verem seus reviews"""
    if 'usuario_id' not in session:
        flash('Você precisa estar logado!', 'warning')
        return redirect(url_for('login'))
    
    if session.get('tipo_usuario') != 3:  # Apenas professores
        flash('Esta página é exclusiva para professores!', 'warning')
        return redirect(url_for('home'))
    
    try:
        # Buscar o professor pelo usuário logado
        usuario = Usuario.query.get(session['usuario_id'])
        if not usuario:
            flash('Usuário não encontrado!', 'danger')
            return redirect(url_for('home'))
        
        # Buscar professor pela matrícula do usuário (que corresponde ao código do professor)
        try:
            codigo_professor = int(usuario.matricula_usuario)
            professor = Professor.query.filter_by(codigo_professor=codigo_professor).first()
            if not professor:
                flash('Professor não encontrado no sistema!', 'danger')
                return redirect(url_for('home'))
        except (ValueError, TypeError):
            flash('Matrícula de professor inválida!', 'danger')
            return redirect(url_for('home'))
        
        # Usar procedure simulada para buscar feedbacks do professor
        print(f"Debug: Buscando feedbacks para professor ID: {professor.codigo_professor}, Nome: {professor.nome_professor}")
        feedbacks_data = ProceduresSimuladas.buscar_feedbacks_professor(professor.codigo_professor)
        print(f"Debug: Encontrados {len(feedbacks_data)} feedbacks para o professor")
        
        # Calcular estatísticas
        if feedbacks_data:
            total_feedbacks = len(feedbacks_data)
            media_qualidade = sum(feedback.qualidade for feedback in feedbacks_data) / total_feedbacks
            media_dificuldade = sum(feedback.nivel_dificuldade for feedback in feedbacks_data) / total_feedbacks
            
            # Agrupar por disciplina
            disciplinas_stats = {}
            for feedback in feedbacks_data:
                disciplina = feedback.nome_disciplina
                if disciplina not in disciplinas_stats:
                    disciplinas_stats[disciplina] = {
                        'total': 0,
                        'qualidade_sum': 0,
                        'dificuldade_sum': 0,
                        'feedbacks': []
                    }
                disciplinas_stats[disciplina]['total'] += 1
                disciplinas_stats[disciplina]['qualidade_sum'] += feedback.qualidade
                disciplinas_stats[disciplina]['dificuldade_sum'] += feedback.nivel_dificuldade
                disciplinas_stats[disciplina]['feedbacks'].append(feedback)
            
            # Calcular médias por disciplina
            for disciplina in disciplinas_stats:
                stats = disciplinas_stats[disciplina]
                stats['media_qualidade'] = stats['qualidade_sum'] / stats['total']
                stats['media_dificuldade'] = stats['dificuldade_sum'] / stats['total']
        else:
            total_feedbacks = 0
            media_qualidade = 0
            media_dificuldade = 0
            disciplinas_stats = {}
        
        return render_template('meus_reviews.html',
                             professor=professor,
                             feedbacks=feedbacks_data,
                             total_feedbacks=total_feedbacks,
                             media_qualidade=round(media_qualidade, 1) if media_qualidade else 0,
                             media_dificuldade=round(media_dificuldade, 1) if media_dificuldade else 0,
                             disciplinas_stats=disciplinas_stats)
    
    except Exception as e:
        flash(f'Erro ao carregar reviews: {str(e)}', 'danger')
        return redirect(url_for('home'))

@app.route('/api/procedure/ranking')
def api_ranking_professores():
    """API que demonstra uso de procedure simulada"""
    try:
        disciplina_id = request.args.get('disciplina_id')
        ranking = ProceduresSimuladas.obter_ranking_professores(disciplina_id)
        
        ranking_data = [
            {
                "codigo_professor": r.codigo_professor,
                "nome_professor": r.nome_professor,
                "nome_disciplina": r.nome_disciplina,
                "media_qualidade": round(r.media_qualidade, 2),
                "media_dificuldade": round(r.media_dificuldade, 2),
                "total_feedbacks": r.total_feedbacks
            }
            for r in ranking
        ]
        
        return jsonify({"sucesso": True, "ranking": ranking_data})
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)