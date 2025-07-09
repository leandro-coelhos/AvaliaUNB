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
            Departamento(codigo_departamento='EST', nome_departamento='Estatística'),
            Departamento(codigo_departamento='QUI', nome_departamento='Química'),
        ]

        for dept in departamentos:
            db.session.add(dept)
        db.session.commit()

        # Criar disciplinas (mais disciplinas para ter variedade)
        disciplinas = [
            # Ciência da Computação
            Disciplina(codigo_disciplina='CIC0004', nome_disciplina='Algoritmos e Programação', fk_codigo_departamento='CIC'),
            Disciplina(codigo_disciplina='CIC0090', nome_disciplina='Banco de Dados', fk_codigo_departamento='CIC'),
            Disciplina(codigo_disciplina='CIC0097', nome_disciplina='Estruturas de Dados', fk_codigo_departamento='CIC'),
            Disciplina(codigo_disciplina='CIC0201', nome_disciplina='Redes de Computadores', fk_codigo_departamento='CIC'),
            Disciplina(codigo_disciplina='CIC0169', nome_disciplina='Engenharia de Software', fk_codigo_departamento='CIC'),

            # Matemática
            Disciplina(codigo_disciplina='MAT0025', nome_disciplina='Cálculo 1', fk_codigo_departamento='MAT'),
            Disciplina(codigo_disciplina='MAT0026', nome_disciplina='Cálculo 2', fk_codigo_departamento='MAT'),
            Disciplina(codigo_disciplina='MAT0116', nome_disciplina='Álgebra Linear', fk_codigo_departamento='MAT'),
            Disciplina(codigo_disciplina='MAT0027', nome_disciplina='Cálculo 3', fk_codigo_departamento='MAT'),

            # Física
            Disciplina(codigo_disciplina='FIS0001', nome_disciplina='Física 1', fk_codigo_departamento='FIS'),
            Disciplina(codigo_disciplina='FIS0002', nome_disciplina='Física 2', fk_codigo_departamento='FIS'),
            Disciplina(codigo_disciplina='FIS0003', nome_disciplina='Física 3', fk_codigo_departamento='FIS'),

            # Engenharia
            Disciplina(codigo_disciplina='ENG0001', nome_disciplina='Introdução à Engenharia', fk_codigo_departamento='ENG'),
            Disciplina(codigo_disciplina='ENG0100', nome_disciplina='Desenho Técnico', fk_codigo_departamento='ENG'),
            Disciplina(codigo_disciplina='ENG0200', nome_disciplina='Mecânica dos Materiais', fk_codigo_departamento='ENG'),

            # Estatística
            Disciplina(codigo_disciplina='EST0001', nome_disciplina='Estatística Descritiva', fk_codigo_departamento='EST'),
            Disciplina(codigo_disciplina='EST0002', nome_disciplina='Probabilidade', fk_codigo_departamento='EST'),

            # Química
            Disciplina(codigo_disciplina='QUI0001', nome_disciplina='Química Geral', fk_codigo_departamento='QUI'),
            Disciplina(codigo_disciplina='QUI0002', nome_disciplina='Química Orgânica', fk_codigo_departamento='QUI'),
        ]

        for disc in disciplinas:
            db.session.add(disc)
        db.session.commit()

        # Criar professores (pelo menos um por disciplina + alguns extras)
        professores = [
            # Professores de Ciência da Computação
            Professor(codigo_professor=1, nome_professor='Prof. João Silva'),
            Professor(codigo_professor=2, nome_professor='Prof. Maria Santos'),
            Professor(codigo_professor=3, nome_professor='Prof. Pedro Costa'),
            Professor(codigo_professor=4, nome_professor='Prof. Ana Oliveira'),
            Professor(codigo_professor=5, nome_professor='Prof. Carlos Lima'),
            Professor(codigo_professor=6, nome_professor='Prof. Fernanda Rocha'),

            # Professores de Matemática
            Professor(codigo_professor=7, nome_professor='Prof. Roberto Alves'),
            Professor(codigo_professor=8, nome_professor='Prof. Juliana Pereira'),
            Professor(codigo_professor=9, nome_professor='Prof. Marcos Vieira'),
            Professor(codigo_professor=10, nome_professor='Prof. Luciana Gomes'),

            # Professores de Física
            Professor(codigo_professor=11, nome_professor='Prof. Eduardo Martins'),
            Professor(codigo_professor=12, nome_professor='Prof. Beatriz Nunes'),
            Professor(codigo_professor=13, nome_professor='Prof. Alexandre Dias'),

            # Professores de Engenharia
            Professor(codigo_professor=14, nome_professor='Prof. Ricardo Monteiro'),
            Professor(codigo_professor=15, nome_professor='Prof. Patrícia Lopes'),
            Professor(codigo_professor=16, nome_professor='Prof. Thiago Ribeiro'),

            # Professores de Estatística
            Professor(codigo_professor=17, nome_professor='Prof. Camila Torres'),
            Professor(codigo_professor=18, nome_professor='Prof. Diego Ferreira'),

            # Professores de Química
            Professor(codigo_professor=19, nome_professor='Prof. Sandra Mendes'),
            Professor(codigo_professor=20, nome_professor='Prof. André Barbosa'),
        ]

        for prof in professores:
            db.session.add(prof)
        db.session.commit()

        # Criar tipos de usuário
        tipos_usuario = [
            TipoUsuario(codigo_tipo_usuario=1, nome_tipo_usuario='Aluno'),
            TipoUsuario(codigo_tipo_usuario=2, nome_tipo_usuario='Administrador'),
            TipoUsuario(codigo_tipo_usuario=3, nome_tipo_usuario='Professor'),
            TipoUsuario(codigo_tipo_usuario=4, nome_tipo_usuario='Departamento'),
            TipoUsuario(codigo_tipo_usuario=5, nome_tipo_usuario='Técnico Administrativo'),
        ]

        for tipo in tipos_usuario:
            db.session.add(tipo)
        db.session.commit()

        # Criar períodos letivos de 2017.1 até 2025.1
        periodos = []
        for ano in range(2017, 2026):  # 2017 a 2025
            if ano == 2025:
                # Para 2025, apenas primeiro semestre
                periodos.append(PeriodoLetivo(ano_periodo=ano, sequencial_periodo=1))
            else:
                # Para outros anos, primeiro e segundo semestres
                periodos.append(PeriodoLetivo(ano_periodo=ano, sequencial_periodo=1))
                periodos.append(PeriodoLetivo(ano_periodo=ano, sequencial_periodo=2))

        for periodo in periodos:
            db.session.add(periodo)
        db.session.commit()

        # Criar usuários (mais alunos para dar feedbacks)
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
            Usuario(
                numero_identificacao_usuario=3,
                nome_usuario='Maria Estudante',
                email_usuario='maria@gmail.com',
                telefone_usuario='61777777777',
                matricula_usuario='190005678',
                senha_usuario=generate_password_hash('123456'),
                fk_codigo_tipo_usuario=1
            ),
            Usuario(
                numero_identificacao_usuario=4,
                nome_usuario='Carlos Discente',
                email_usuario='carlos@gmail.com',
                telefone_usuario='61666666666',
                matricula_usuario='190009012',
                senha_usuario=generate_password_hash('123456'),
                fk_codigo_tipo_usuario=1
            ),
            Usuario(
                numero_identificacao_usuario=5,
                nome_usuario='Ana Acadêmica',
                email_usuario='ana@gmail.com',
                telefone_usuario='61555555555',
                matricula_usuario='190003456',
                senha_usuario=generate_password_hash('123456'),
                fk_codigo_tipo_usuario=1
            ),
        ]

        for usuario in usuarios:
            db.session.add(usuario)
        db.session.commit()

        # Criar turmas para todos os períodos
        turmas = []
        numero_turma = 1
        
        # Disciplinas principais que terão turmas em todos os períodos
        disciplinas_principais = ['CIC0004', 'MAT0025', 'FIS0001', 'ENG0001']
        
        # Criar turmas para cada período de 2017.1 até 2025.1
        for ano in range(2017, 2026):
            semestres = [1, 2] if ano < 2025 else [1]  # 2025 só tem semestre 1
            
            for semestre in semestres:
                periodo_codigo = f"{ano}.{semestre}"
                
                # Para cada período, criar pelo menos 4 turmas das disciplinas principais
                for disciplina_codigo in disciplinas_principais:
                    turmas.append(Turma(
                        numero_identificacao_turma=numero_turma,
                        fk_codigo_disciplina=disciplina_codigo,
                        fk_codigo_periodo=periodo_codigo
                    ))
                    numero_turma += 1
                
                # Adicionar mais algumas disciplinas aleatoriamente para variedade
                if ano >= 2020:  # A partir de 2020, adicionar mais disciplinas
                    disciplinas_extras = ['CIC0090', 'MAT0026', 'FIS0002', 'ENG0100', 'EST0001', 'QUI0001']
                    for i, disciplina_codigo in enumerate(disciplinas_extras):
                        if (ano + semestre + i) % 3 == 0:  # Distribuir de forma pseudo-aleatória
                            turmas.append(Turma(
                                numero_identificacao_turma=numero_turma,
                                fk_codigo_disciplina=disciplina_codigo,
                                fk_codigo_periodo=periodo_codigo
                            ))
                            numero_turma += 1
                
                # Para períodos mais recentes (2023+), adicionar ainda mais variedade
                if ano >= 2023:
                    todas_disciplinas = [
                        'CIC0097', 'CIC0201', 'CIC0169', 'MAT0116', 'MAT0027', 
                        'FIS0003', 'ENG0200', 'EST0002', 'QUI0002'
                    ]
                    for i, disciplina_codigo in enumerate(todas_disciplinas):
                        if (ano + semestre + i) % 4 == 0:  # Mais seletivo
                            turmas.append(Turma(
                                numero_identificacao_turma=numero_turma,
                                fk_codigo_disciplina=disciplina_codigo,
                                fk_codigo_periodo=periodo_codigo
                            ))
                            numero_turma += 1

        for turma in turmas:
            db.session.add(turma)
        db.session.commit()

        # Criar tipos de avaliação
        tipos_avaliacao = [
            TipoAvaliacao(codigo_tipo_avaliacao=1, nome_tipo_avaliacao='Prova'),
            TipoAvaliacao(codigo_tipo_avaliacao=2, nome_tipo_avaliacao='Trabalho'),
            TipoAvaliacao(codigo_tipo_avaliacao=3, nome_tipo_avaliacao='Plano de Ensino'),
            TipoAvaliacao(codigo_tipo_avaliacao=4, nome_tipo_avaliacao='Projeto'),
            TipoAvaliacao(codigo_tipo_avaliacao=5, nome_tipo_avaliacao='Apresentação'),
        ]

        for tipo_aval in tipos_avaliacao:
            db.session.add(tipo_aval)
        db.session.commit()

        # Criar critérios de avaliação para algumas turmas
        criterios = [
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=1, fk_numero_identificacao_turma=1, fk_codigo_tipo_avaliacao=1),
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=2, fk_numero_identificacao_turma=2, fk_codigo_tipo_avaliacao=1),
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=3, fk_numero_identificacao_turma=3, fk_codigo_tipo_avaliacao=1),
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=4, fk_numero_identificacao_turma=6, fk_codigo_tipo_avaliacao=1),
            CriterioAvaliacaoTurma(numero_identificacao_avaliacao=5, fk_numero_identificacao_turma=10, fk_codigo_tipo_avaliacao=1),
        ]

        for criterio in criterios:
            db.session.add(criterio)
        db.session.commit()

        # Criar feedbacks extensivos (pelo menos um por professor + alguns extras)
        feedbacks_exemplo = [
            # Feedbacks para professores de Ciência da Computação
            Feedback(pfk_numero_identificacao_turma=1, pfk_codigo_professor=1, pfk_numero_identificacao_usuario=1, nivel_dificuldade=3, qualidade=4, comentario='Excelente professor, explica muito bem!'),
            Feedback(pfk_numero_identificacao_turma=1, pfk_codigo_professor=1, pfk_numero_identificacao_usuario=3, nivel_dificuldade=4, qualidade=5, comentario='Aulas dinâmicas e bem estruturadas.'),

            Feedback(pfk_numero_identificacao_turma=2, pfk_codigo_professor=2, pfk_numero_identificacao_usuario=1, nivel_dificuldade=4, qualidade=5, comentario='Matéria difícil mas a professora é ótima!'),
            Feedback(pfk_numero_identificacao_turma=2, pfk_codigo_professor=2, pfk_numero_identificacao_usuario=4, nivel_dificuldade=3, qualidade=4, comentario='Muito didática e paciente.'),

            Feedback(pfk_numero_identificacao_turma=3, pfk_codigo_professor=3, pfk_numero_identificacao_usuario=1, nivel_dificuldade=5, qualidade=3, comentario='Matéria complexa, professor poderia melhorar didática.'),
            Feedback(pfk_numero_identificacao_turma=3, pfk_codigo_professor=3, pfk_numero_identificacao_usuario=5, nivel_dificuldade=4, qualidade=4, comentario='Bom domínio do conteúdo.'),

            Feedback(pfk_numero_identificacao_turma=4, pfk_codigo_professor=4, pfk_numero_identificacao_usuario=3, nivel_dificuldade=3, qualidade=5, comentario='Professora excepcional! Recomendo muito.'),

            Feedback(pfk_numero_identificacao_turma=5, pfk_codigo_professor=5, pfk_numero_identificacao_usuario=4, nivel_dificuldade=4, qualidade=4, comentario='Aulas práticas muito úteis.'),

            Feedback(pfk_numero_identificacao_turma=20, pfk_codigo_professor=6, pfk_numero_identificacao_usuario=5, nivel_dificuldade=2, qualidade=5, comentario='Professora incrível, faz a matéria parecer fácil!'),

            # Feedbacks para professores de Matemática
            Feedback(pfk_numero_identificacao_turma=6, pfk_codigo_professor=7, pfk_numero_identificacao_usuario=1, nivel_dificuldade=5, qualidade=3, comentario='Cálculo é difícil, professor ok.'),
            Feedback(pfk_numero_identificacao_turma=6, pfk_codigo_professor=7, pfk_numero_identificacao_usuario=3, nivel_dificuldade=4, qualidade=4, comentario='Explica bem os conceitos básicos.'),

            Feedback(pfk_numero_identificacao_turma=7, pfk_codigo_professor=8, pfk_numero_identificacao_usuario=4, nivel_dificuldade=4, qualidade=5, comentario='Excelente professora de matemática!'),

            Feedback(pfk_numero_identificacao_turma=8, pfk_codigo_professor=9, pfk_numero_identificacao_usuario=1, nivel_dificuldade=3, qualidade=4, comentario='Álgebra linear bem explicada.'),

            Feedback(pfk_numero_identificacao_turma=9, pfk_codigo_professor=10, pfk_numero_identificacao_usuario=5, nivel_dificuldade=5, qualidade=4, comentario='Cálculo 3 é pesado, mas ela ajuda muito.'),

            Feedback(pfk_numero_identificacao_turma=21, pfk_codigo_professor=7, pfk_numero_identificacao_usuario=4, nivel_dificuldade=4, qualidade=3, comentario='Segunda vez com ele, melhorou um pouco.'),

            # Feedbacks para professores de Física
            Feedback(pfk_numero_identificacao_turma=10, pfk_codigo_professor=11, pfk_numero_identificacao_usuario=3, nivel_dificuldade=4, qualidade=4, comentario='Física experimental muito boa.'),

            Feedback(pfk_numero_identificacao_turma=11, pfk_codigo_professor=12, pfk_numero_identificacao_usuario=1, nivel_dificuldade=3, qualidade=5, comentario='Melhor professora de física que já tive!'),

            Feedback(pfk_numero_identificacao_turma=12, pfk_codigo_professor=13, pfk_numero_identificacao_usuario=5, nivel_dificuldade=5, qualidade=3, comentario='Física 3 é complicada, professor razoável.'),

            # Feedbacks para professores de Engenharia
            Feedback(pfk_numero_identificacao_turma=13, pfk_codigo_professor=14, pfk_numero_identificacao_usuario=4, nivel_dificuldade=2, qualidade=4, comentario='Boa introdução à engenharia.'),

            Feedback(pfk_numero_identificacao_turma=14, pfk_codigo_professor=15, pfk_numero_identificacao_usuario=3, nivel_dificuldade=3, qualidade=4, comentario='Desenho técnico bem ensinado.'),

            Feedback(pfk_numero_identificacao_turma=15, pfk_codigo_professor=16, pfk_numero_identificacao_usuario=1, nivel_dificuldade=4, qualidade=5, comentario='Professor muito competente!'),

            # Feedbacks para professores de Estatística
            Feedback(pfk_numero_identificacao_turma=16, pfk_codigo_professor=17, pfk_numero_identificacao_usuario=5, nivel_dificuldade=2, qualidade=5, comentario='Estatística nunca foi tão fácil!'),

            Feedback(pfk_numero_identificacao_turma=17, pfk_codigo_professor=18, pfk_numero_identificacao_usuario=3, nivel_dificuldade=4, qualidade=4, comentario='Probabilidade bem explicada.'),

            # Feedbacks para professores de Química
            Feedback(pfk_numero_identificacao_turma=18, pfk_codigo_professor=19, pfk_numero_identificacao_usuario=4, nivel_dificuldade=3, qualidade=4, comentario='Química geral interessante.'),

            Feedback(pfk_numero_identificacao_turma=19, pfk_codigo_professor=20, pfk_numero_identificacao_usuario=1, nivel_dificuldade=4, qualidade=3, comentario='Orgânica é difícil, professor ok.'),

            # Alguns feedbacks extras para ter mais variedade
            Feedback(pfk_numero_identificacao_turma=1, pfk_codigo_professor=1, pfk_numero_identificacao_usuario=4, nivel_dificuldade=2, qualidade=5, comentario='Melhor professor de programação!'),
            Feedback(pfk_numero_identificacao_turma=6, pfk_codigo_professor=7, pfk_numero_identificacao_usuario=5, nivel_dificuldade=5, qualidade=2, comentario='Muito difícil de entender.'),
            Feedback(pfk_numero_identificacao_turma=10, pfk_codigo_professor=11, pfk_numero_identificacao_usuario=4, nivel_dificuldade=3, qualidade=4, comentario='Laboratório bem organizado.'),
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
        print("Aluna: maria@gmail.com / 123456")
        print("Aluno: carlos@gmail.com / 123456")
        print("Aluna: ana@gmail.com / 123456")
        print("Admin: admin@unb.br / admin123")
        print("==================================")
        print("\n=== ESTATÍSTICAS DO BANCO ===")
        print(f"Departamentos: {len(departamentos)}")
        print(f"Disciplinas: {len(disciplinas)}")
        print(f"Professores: {len(professores)}")
        print(f"Usuários: {len(usuarios)}")
        print(f"Turmas: {len(turmas)}")
        print(f"Feedbacks: {len(feedbacks_exemplo)}")
        print("===============================")

if __name__ == '__main__':
    popular_banco()