
from models import db, Professor, Feedback, Usuario, Turma, Disciplina
from sqlalchemy import text, func
from flask import current_app

class ProceduresSimuladas:
    """Classe que simula stored procedures usando funções Python"""
    
    @staticmethod
    def listar_professores_com_feedbacks():
        """Simula: CALL ListarProfessoresComFeedbacks()"""
        try:
            resultado = db.session.execute(text("""
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
            return resultado.fetchall()
        except Exception as e:
            print(f"Erro ao listar professores: {e}")
            return []
    
    @staticmethod
    def buscar_feedbacks_professor(professor_id):
        """Simula: CALL BuscarFeedbacksProfessor(:prof_id)"""
        try:
            print(f"Debug: Executando query para professor_id = {professor_id}")
            resultado = db.session.execute(text("""
            SELECT f.pfk_Num_Idf_Tur as turma_id,
                   f.pfk_Cod_Prof as professor_id,
                   f.pfk_Num_Idf_Usr as usuario_id,
                   f.Nvl_Dif as nivel_dificuldade,
                   f.Qual as qualidade,
                   f.Coment as comentario,
                   u.Nom_Usr as nome_usuario,
                   t.Num_Idf_Tur as numero_turma,
                   d.Nom_Dis as nome_disciplina,
                   d.Cod_Dis as disciplina_codigo,
                   p.Nom_Prof as nome_professor
            FROM Fdbk f
            JOIN Usr u ON f.pfk_Num_Idf_Usr = u.Num_Idf_Usr
            JOIN Tur t ON f.pfk_Num_Idf_Tur = t.Num_Idf_Tur
            JOIN Dis d ON t.fk_Cod_Dis = d.Cod_Dis
            JOIN Prof p ON f.pfk_Cod_Prof = p.Cod_Prof
            WHERE f.pfk_Cod_Prof = :prof_id
            ORDER BY f.Qual DESC, f.Nvl_Dif ASC
            """), {"prof_id": professor_id})
            feedbacks = resultado.fetchall()
            print(f"Debug: Query retornou {len(feedbacks)} feedbacks")
            return feedbacks
        except Exception as e:
            print(f"Erro ao buscar feedbacks do professor: {e}")
            return []
    
    @staticmethod
    def calcular_media_professor(professor_id):
        """Simula: CALL CalcularMediaProfessor(:prof_id)"""
        try:
            resultado = db.session.execute(text("""
            SELECT AVG(f.Qual) as media_qualidade,
                   AVG(f.Nvl_Dif) as media_dificuldade,
                   COUNT(*) as total_feedbacks
            FROM Fdbk f
            WHERE f.pfk_Cod_Prof = :prof_id
            """), {"prof_id": professor_id})
            return resultado.fetchone()
        except Exception as e:
            print(f"Erro ao calcular média do professor: {e}")
            return None
    
    @staticmethod
    def inserir_feedback_completo(dados_feedback):
        """Simula: CALL InserirFeedbackCompleto(...)"""
        try:
            # Verificar se já existe feedback
            feedback_existente = Feedback.query.filter_by(
                pfk_numero_identificacao_turma=dados_feedback['turma_id'],
                pfk_codigo_professor=dados_feedback['professor_id'],
                pfk_numero_identificacao_usuario=dados_feedback['usuario_id']
            ).first()
            
            if feedback_existente:
                return {"sucesso": False, "mensagem": "Feedback já existe"}
            
            # Inserir novo feedback
            novo_feedback = Feedback(
                pfk_numero_identificacao_turma=dados_feedback['turma_id'],
                pfk_codigo_professor=dados_feedback['professor_id'],
                pfk_numero_identificacao_usuario=dados_feedback['usuario_id'],
                nivel_dificuldade=dados_feedback['dificuldade'],
                qualidade=dados_feedback['qualidade'],
                comentario=dados_feedback['comentario']
            )
            
            db.session.add(novo_feedback)
            db.session.commit()
            
            return {"sucesso": True, "mensagem": "Feedback inserido com sucesso"}
            
        except Exception as e:
            db.session.rollback()
            return {"sucesso": False, "mensagem": f"Erro: {str(e)}"}
    
    @staticmethod
    def obter_ranking_professores(disciplina_id=None):
        """Simula: CALL ObterRankingProfessores(:disciplina_id)"""
        try:
            query = """
            SELECT p.Cod_Prof as codigo_professor,
                   p.Nom_Prof as nome_professor,
                   d.Nom_Dis as nome_disciplina,
                   AVG(f.Qual) as media_qualidade,
                   AVG(f.Nvl_Dif) as media_dificuldade,
                   COUNT(f.pfk_Cod_Prof) as total_feedbacks
            FROM Prof p
            JOIN Fdbk f ON p.Cod_Prof = f.pfk_Cod_Prof
            JOIN Tur t ON f.pfk_Num_Idf_Tur = t.Num_Idf_Tur
            JOIN Dis d ON t.fk_Cod_Dis = d.Cod_Dis
            """
            
            if disciplina_id:
                query += " WHERE d.Cod_Dis = :disciplina_id"
                params = {"disciplina_id": disciplina_id}
            else:
                params = {}
            
            query += """
            GROUP BY p.Cod_Prof, p.Nom_Prof, d.Nom_Dis
            ORDER BY AVG(f.Qual) DESC, COUNT(f.pfk_Cod_Prof) DESC
            """
            
            resultado = db.session.execute(text(query), params)
            return resultado.fetchall()
            
        except Exception as e:
            print(f"Erro ao obter ranking: {e}")
            return []
    
    @staticmethod
    def buscar_turmas_professor(professor_id):
        """Simula: CALL BuscarTurmasProfessor(:prof_id)"""
        try:
            resultado = db.session.execute(text("""
            SELECT DISTINCT t.Num_Idf_Tur as turma_id,
                   d.Cod_Dis as disciplina_codigo,
                   d.Nom_Dis as nome_disciplina,
                   pl.Cod_Per as periodo_codigo,
                   COUNT(f.pfk_Num_Idf_Tur) as total_feedbacks
            FROM Tur t
            JOIN Dis d ON t.fk_Cod_Dis = d.Cod_Dis
            JOIN Per_Let pl ON t.fk_Cod_Per = pl.Cod_Per
            LEFT JOIN Fdbk f ON t.Num_Idf_Tur = f.pfk_Num_Idf_Tur AND f.pfk_Cod_Prof = :prof_id
            WHERE EXISTS (
                SELECT 1 FROM Fdbk f2 
                WHERE f2.pfk_Num_Idf_Tur = t.Num_Idf_Tur 
                AND f2.pfk_Cod_Prof = :prof_id
            )
            GROUP BY t.Num_Idf_Tur, d.Cod_Dis, d.Nom_Dis, pl.Cod_Per
            ORDER BY pl.Cod_Per DESC, d.Nom_Dis
            """), {"prof_id": professor_id})
            return resultado.fetchall()
        except Exception as e:
            print(f"Erro ao buscar turmas do professor: {e}")
            return []
    
    @staticmethod
    def obter_estatisticas_sistema():
        """Simula: CALL ObterEstatisticasSistema()"""
        try:
            # Usar SQLAlchemy ORM para estatísticas simples
            stats = {
                'total_professores': Professor.query.count(),
                'total_usuarios': Usuario.query.count(),
                'total_feedbacks': Feedback.query.count(),
                'total_disciplinas': Disciplina.query.count(),
                'total_turmas': Turma.query.count()
            }
            
            # Buscar médias gerais
            resultado_medias = db.session.execute(text("""
            SELECT AVG(Qual) as media_geral_qualidade,
                   AVG(Nvl_Dif) as media_geral_dificuldade
            FROM Fdbk
            """))
            medias = resultado_medias.fetchone()
            
            if medias:
                stats['media_geral_qualidade'] = round(medias.media_geral_qualidade or 0, 2)
                stats['media_geral_dificuldade'] = round(medias.media_geral_dificuldade or 0, 2)
            
            return stats
            
        except Exception as e:
            print(f"Erro ao obter estatísticas: {e}")
            return {}
