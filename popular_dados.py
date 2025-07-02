
from models import db, Professor, Disciplina, Departamento, Turma, PeriodoLetivo
from main import app

def popular_dados():
    with app.app_context():
        # Criar departamentos
        if not Departamento.query.first():
            departamentos = [
                Departamento(Cod_Dep='CIC', Nom_Dep='Ciência da Computação'),
                Departamento(Cod_Dep='MAT', Nom_Dep='Matemática'),
                Departamento(Cod_Dep='FIS', Nom_Dep='Física'),
                Departamento(Cod_Dep='ENG', Nom_Dep='Engenharia'),
                Departamento(Cod_Dep='ADM', Nom_Dep='Administração')
            ]
            
            for dep in departamentos:
                db.session.add(dep)
        
        # Criar professores
        if not Professor.query.first():
            professores = [
                Professor(Cod_Prof=1, Nom_Prof='Prof. João Silva'),
                Professor(Cod_Prof=2, Nom_Prof='Prof. Maria Santos'),
                Professor(Cod_Prof=3, Nom_Prof='Prof. Carlos Oliveira'),
                Professor(Cod_Prof=4, Nom_Prof='Prof. Ana Costa'),
                Professor(Cod_Prof=5, Nom_Prof='Prof. Pedro Lima'),
                Professor(Cod_Prof=6, Nom_Prof='Prof. Julia Rocha'),
                Professor(Cod_Prof=7, Nom_Prof='Prof. Roberto Alves'),
                Professor(Cod_Prof=8, Nom_Prof='Prof. Fernanda Dias'),
                Professor(Cod_Prof=9, Nom_Prof='Prof. Lucas Martins'),
                Professor(Cod_Prof=10, Nom_Prof='Prof. Beatriz Ferreira')
            ]
            
            for prof in professores:
                db.session.add(prof)
        
        # Criar períodos letivos
        if not PeriodoLetivo.query.first():
            periodos = [
                PeriodoLetivo(Cod_Per='2024-1', Ano_Per=2024, Seq_Per=1),
                PeriodoLetivo(Cod_Per='2024-2', Ano_Per=2024, Seq_Per=2),
                PeriodoLetivo(Cod_Per='2025-1', Ano_Per=2025, Seq_Per=1)
            ]
            
            for periodo in periodos:
                db.session.add(periodo)
        
        # Criar disciplinas
        if not Disciplina.query.first():
            disciplinas = [
                Disciplina(Cod_Dis='CIC0004', Nom_Dis='Algoritmos', fk_Cod_Dep='CIC'),
                Disciplina(Cod_Dis='CIC0097', Nom_Dis='Banco de Dados', fk_Cod_Dep='CIC'),
                Disciplina(Cod_Dis='MAT0025', Nom_Dis='Cálculo 1', fk_Cod_Dep='MAT'),
                Disciplina(Cod_Dis='MAT0026', Nom_Dis='Cálculo 2', fk_Cod_Dep='MAT'),
                Disciplina(Cod_Dis='FIS0201', Nom_Dis='Física 1', fk_Cod_Dep='FIS'),
                Disciplina(Cod_Dis='ENG0001', Nom_Dis='Programação', fk_Cod_Dep='ENG'),
                Disciplina(Cod_Dis='ADM0001', Nom_Dis='Gestão', fk_Cod_Dep='ADM'),
                Disciplina(Cod_Dis='CIC0090', Nom_Dis='Estrutura de Dados', fk_Cod_Dep='CIC'),
                Disciplina(Cod_Dis='MAT0027', Nom_Dis='Álgebra Linear', fk_Cod_Dep='MAT'),
                Disciplina(Cod_Dis='CIC0201', Nom_Dis='Redes', fk_Cod_Dep='CIC')
            ]
            
            for disc in disciplinas:
                db.session.add(disc)
        
        # Criar turmas
        if not Turma.query.first():
            turmas = [
                Turma(Num_Idf_Tur=1, fk_Cod_Dis='CIC0004', fk_Cod_Per='2024-1'),
                Turma(Num_Idf_Tur=2, fk_Cod_Dis='CIC0097', fk_Cod_Per='2024-1'),
                Turma(Num_Idf_Tur=3, fk_Cod_Dis='MAT0025', fk_Cod_Per='2024-1'),
                Turma(Num_Idf_Tur=4, fk_Cod_Dis='MAT0026', fk_Cod_Per='2024-2'),
                Turma(Num_Idf_Tur=5, fk_Cod_Dis='FIS0201', fk_Cod_Per='2024-2'),
                Turma(Num_Idf_Tur=6, fk_Cod_Dis='ENG0001', fk_Cod_Per='2024-2'),
                Turma(Num_Idf_Tur=7, fk_Cod_Dis='ADM0001', fk_Cod_Per='2025-1'),
                Turma(Num_Idf_Tur=8, fk_Cod_Dis='CIC0090', fk_Cod_Per='2025-1'),
                Turma(Num_Idf_Tur=9, fk_Cod_Dis='MAT0027', fk_Cod_Per='2025-1'),
                Turma(Num_Idf_Tur=10, fk_Cod_Dis='CIC0201', fk_Cod_Per='2025-1'),
                Turma(Num_Idf_Tur=11, fk_Cod_Dis='CIC0004', fk_Cod_Per='2024-2'),
                Turma(Num_Idf_Tur=12, fk_Cod_Dis='CIC0097', fk_Cod_Per='2025-1')
            ]
            
            for turma in turmas:
                db.session.add(turma)
        
        # Salvar tudo
        db.session.commit()
        print("Dados populados com sucesso!")

if __name__ == '__main__':
    popular_dados()
