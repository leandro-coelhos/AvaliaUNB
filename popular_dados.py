from main import app, db
from models import (Departamento, Disciplina, Professor, TipoUsuario, 
                   Usuario, PeriodoLetivo, Turma, TipoAvaliacao, 
                   CriterioAvaliacaoTurma, DocumentoAvaliacao, Feedback)
from werkzeug.security import generate_password_hash

def popular_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()

        departamentos = [
            Departamento(codigo_departamento='CIC', nome_departamento='Ciência da Computação'),
            Departamento(codigo_departamento='MAT', nome_departamento='Matemática'),
            Departamento(codigo_departamento='FIS', nome_departamento='Física'),
            Departamento(codigo_departamento='ENG', nome_departamento='Engenharia'),
        ]

        for dept in departamentos:
            db.session.add(dept)
        db.session.commit()

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

        tipos_usuario = [
            TipoUsuario(codigo_tipo_usuario=1, nome_tipo_usuario='Aluno'),
            TipoUsuario(codigo_tipo_usuario=2, nome_tipo_usuario='Administrador'),
        ]

        for tipo in tipos_usuario:
            db.session.add(tipo)
        db.session.commit()

        usuarios = [
            Usuario(
                numero_identificacao_usuario=1,
                nome_usuario='João Admin',
                email_usuario='joao@admin.unb.br',
                telefone_usuario='(61) 99999-1111',
                matricula_usuario='admin123',
                fk_codigo_tipo_usuario=2
            ),
            Usuario(
                numero_identificacao_usuario=2,
                nome_usuario='Maria Estudante',
                email_usuario='maria@aluno.unb.br',
                telefone_usuario='(61) 99999-2222',
                matricula_usuario='22222222',
                fk_codigo_tipo_usuario=1
            ),
            Usuario(
                numero_identificacao_usuario=3,
                nome_usuario='Pedro Estudante',
                email_usuario='pedro@aluno.unb.br',
                telefone_usuario='(61) 99999-3333',
                matricula_usuario='11111111',
                fk_codigo_tipo_usuario=1
            ),
        ]

        for usuario in usuarios:
            db.session.add(usuario)
        db.session.commit()

        periodos = [
            PeriodoLetivo(codigo_periodo='2024-1', ano_periodo=2024, sequencial_periodo=1),
            PeriodoLetivo(codigo_periodo='2024-2', ano_periodo=2024, sequencial_periodo=2),
            PeriodoLetivo(codigo_periodo='2023-1', ano_periodo=2023, sequencial_periodo=1),
        ]

        for periodo in periodos:
            db.session.add(periodo)
        db.session.commit()

        turmas = [
            Turma(numero_identificacao_turma=1, fk_codigo_disciplina='CIC0004', fk_codigo_periodo='2024-1'),
            Turma(numero_identificacao_turma=2, fk_codigo_disciplina='CIC0090', fk_codigo_periodo='2024-1'),
            Turma(numero_identificacao_turma=3, fk_codigo_disciplina='MAT0025', fk_codigo_periodo='2024-1'),
            Turma(numero_identificacao_turma=4, fk_codigo_disciplina='FIS0001', fk_codigo_periodo='2024-2'),
            Turma(numero_identificacao_turma=5, fk_codigo_disciplina='ENG0001', fk_codigo_periodo='2024-2'),
        ]

        for turma in turmas:
            db.session.add(turma)
        db.session.commit()

        tipos_avaliacao = [
            TipoAvaliacao(codigo_tipo_avaliacao=1, nome_tipo_avaliacao='Prova'),
            TipoAvaliacao(codigo_tipo_avaliacao=2, nome_tipo_avaliacao='Trabalho'),
            TipoAvaliacao(codigo_tipo_avaliacao=3, nome_tipo_avaliacao='Seminário'),
        ]

        for tipo_aval in tipos_avaliacao:
            db.session.add(tipo_aval)
        db.session.commit()

        criterios_avaliacao = [
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=1, fk_numero_identificacao_turma=1, fk_codigo_tipo_avaliacao=1),
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=2, fk_numero_identificacao_turma=1, fk_codigo_tipo_avaliacao=2),
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=3, fk_numero_identificacao_turma=2, fk_codigo_tipo_avaliacao=1),
        ]

        for criterio in criterios_avaliacao:
            db.session.add(criterio)
        db.session.commit()

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
                pfk_numero_identificacao_usuario=3,
                nivel_dificuldade=2,
                qualidade=3,
                comentario='Aulas interessantes, poderia dar mais exemplos.'
            ),
        ]

        for feedback in feedbacks_exemplo:
            db.session.add(feedback)
        db.session.commit()

        print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    popular_banco()