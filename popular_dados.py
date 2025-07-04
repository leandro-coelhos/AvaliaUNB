
from main import app, db
from models import (Departamento, Disciplina, Professor, TipoUsuario, 
                   Usuario, PeriodoLetivo, Turma, TipoAvaliacao, 
                   CriterioAvaliacaoTurma, DocumentoAvaliacao, Feedback)
from werkzeug.security import generate_password_hash
from sqlalchemy import text

def popular_banco():
    with app.app_context():
        # Recriar todas as tabelas
        db.drop_all()
        db.create_all()

        # Criar departamentos
        departamentos = [
            Departamento(codigo_departamento='CIC', nome_departamento='Ciência da Computação'),
            Departamento(codigo_departamento='MAT', nome_departamento='Matemática'),
            Departamento(codigo_departamento='FIS', nome_departamento='Física'),
            Departamento(codigo_departamento='ENG', nome_departamento='Engenharia'),
        ]

        for dept in departamentos:
            db.session.add(dept)
        db.session.commit()

        # Criar disciplinas
        disciplinas = [
            Disciplina(codigo_disciplina='CIC0004', nome_disciplina='Algoritmos e Programação', fk_codigo_departamento='CIC'),
            Disciplina(codigo_disciplina='CIC0090', nome_disciplina='Banco de Dados', fk_codigo_departamento='CIC'),
            Disciplina(codigo_disciplina='MAT0025', nome_disciplina='Cálculo 1', fk_codigo_departamento='MAT'),
            Disciplina(codigo_disciplina='FIS0001', nome_disciplina='Física 1', fk_codigo_departamento='FIS'),
            Disciplina(codigo_disciplina='ENG0001', nome_disciplina='Introdução à Engenharia', fk_codigo_departamento='ENG'),
        ]

        for disc in disciplinas:
            db.session.add(disc)
        db.session.commit()

        # Criar professores
        professores = [
            Professor(codigo_professor=1, nome_professor='Prof. João Silva'),
            Professor(codigo_professor=2, nome_professor='Prof. Maria Santos'),
            Professor(codigo_professor=3, nome_professor='Prof. Pedro Costa'),
            Professor(codigo_professor=4, nome_professor='Prof. Ana Oliveira'),
            Professor(codigo_professor=5, nome_professor='Prof. Carlos Lima'),
        ]

        for prof in professores:
            db.session.add(prof)
        db.session.commit()

        # Criar tipos de usuário
        tipos_usuario = [
            TipoUsuario(codigo_tipo_usuario=1, nome_tipo_usuario='Aluno'),
            TipoUsuario(codigo_tipo_usuario=2, nome_tipo_usuario='Administrador'),
        ]

        for tipo in tipos_usuario:
            db.session.add(tipo)
        db.session.commit()

        # Criar períodos letivos
        periodos = [
            PeriodoLetivo(codigo_periodo='2024.1', ano_periodo=2024, sequencial_periodo=1),
            PeriodoLetivo(codigo_periodo='2024.2', ano_periodo=2024, sequencial_periodo=2),
        ]

        for periodo in periodos:
            db.session.add(periodo)
        db.session.commit()

        # Criar usuários
        usuarios = [
            Usuario(
                numero_identificacao_usuario=1,
                nome_usuario='João Aluno',
                email_usuario='joao@gmail.com',
                telefone_usuario='61999999999',
                matricula_usuario='190001234',
                senha_usuario=generate_password_hash('123456'),
                fk_codigo_tipo_usuario=1
            ),
            Usuario(
                numero_identificacao_usuario=2,
                nome_usuario='Admin Sistema',
                email_usuario='admin@unb.br',
                telefone_usuario='61888888888',
                matricula_usuario='ADM001',
                senha_usuario=generate_password_hash('admin123'),
                fk_codigo_tipo_usuario=2
            ),
        ]

        for usuario in usuarios:
            db.session.add(usuario)
        db.session.commit()

        # Criar turmas
        turmas = [
            Turma(numero_identificacao_turma=1, fk_codigo_disciplina='CIC0004', fk_codigo_periodo='2024.1'),
            Turma(numero_identificacao_turma=2, fk_codigo_disciplina='CIC0090', fk_codigo_periodo='2024.1'),
            Turma(numero_identificacao_turma=3, fk_codigo_disciplina='MAT0025', fk_codigo_periodo='2024.1'),
            Turma(numero_identificacao_turma=4, fk_codigo_disciplina='FIS0001', fk_codigo_periodo='2024.2'),
            Turma(numero_identificacao_turma=5, fk_codigo_disciplina='ENG0001', fk_codigo_periodo='2024.2'),
        ]

        for turma in turmas:
            db.session.add(turma)
        db.session.commit()

        # Criar tipos de avaliação
        tipos_avaliacao = [
            TipoAvaliacao(codigo_tipo_avaliacao=1, nome_tipo_avaliacao='Feedback Geral'),
            TipoAvaliacao(codigo_tipo_avaliacao=2, nome_tipo_avaliacao='Avaliação Formal'),
        ]

        for tipo_aval in tipos_avaliacao:
            db.session.add(tipo_aval)
        db.session.commit()

        # Criar critérios de avaliação
        criterios = [
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=1, fk_numero_identificacao_turma=1, fk_codigo_tipo_avaliacao=1),
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=2, fk_numero_identificacao_turma=2, fk_codigo_tipo_avaliacao=1),
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=3, fk_numero_identificacao_turma=3, fk_codigo_tipo_avaliacao=1),
        ]

        for criterio in criterios:
            db.session.add(criterio)
        db.session.commit()

        # Criar feedbacks de exemplo
        feedbacks_exemplo = [
            Feedback(
                pfk_numero_identificacao_turma=1,
                pfk_codigo_professor=1,
                pfk_numero_identificacao_usuario=1,
                nivel_dificuldade=3,
                qualidade=4,
                comentario='Excelente professor, explica muito bem!'
            ),
            Feedback(
                pfk_numero_identificacao_turma=2,
                pfk_codigo_professor=2,
                pfk_numero_identificacao_usuario=1,
                nivel_dificuldade=4,
                qualidade=5,
                comentario='Matéria difícil mas a professora é ótima!'
            ),
            Feedback(
                pfk_numero_identificacao_turma=1,
                pfk_codigo_professor=1,
                pfk_numero_identificacao_usuario=2,
                nivel_dificuldade=2,
                qualidade=3,
                comentario='Aulas interessantes, poderia dar mais exemplos.'
            ),
        ]

        for feedback in feedbacks_exemplo:
            db.session.add(feedback)
        db.session.commit()

        # Criar views SQLite necessárias
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
                   p.Nom_Prof as nome_professor
            FROM Fdbk f
            JOIN Usr u ON f.pfk_Num_Idf_Usr = u.Num_Idf_Usr
            JOIN Tur t ON f.pfk_Num_Idf_Tur = t.Num_Idf_Tur
            JOIN Dis d ON t.fk_Cod_Dis = d.Cod_Dis
            JOIN Prof p ON f.pfk_Cod_Prof = p.Cod_Prof
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
                   d.Nom_Dis as nome_disciplina
            FROM Fdbk f
            JOIN Usr u ON f.pfk_Num_Idf_Usr = u.Num_Idf_Usr
            JOIN Prof p ON f.pfk_Cod_Prof = p.Cod_Prof
            JOIN Tur t ON f.pfk_Num_Idf_Tur = t.Num_Idf_Tur
            JOIN Dis d ON t.fk_Cod_Dis = d.Cod_Dis
            """))
            
            db.session.commit()
            print("Views criadas com sucesso!")
        except Exception as e:
            print(f"Erro ao criar views: {e}")
            db.session.rollback()

        print("Banco de dados populado com sucesso!")
        print("\n=== DADOS DE LOGIN PARA TESTE ===")
        print("Aluno: joao@gmail.com / 123456")
        print("Admin: admin@unb.br / admin123")
        print("==================================")

if __name__ == '__main__':
    popular_banco()
