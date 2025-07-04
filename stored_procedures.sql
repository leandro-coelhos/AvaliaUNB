-- SQLite não suporta stored procedures nativamente
-- Convertendo para views que podem ser consultadas

-- View para listar professores com feedbacks
CREATE VIEW IF NOT EXISTS view_professores_com_feedbacks AS
SELECT p.Cod_Prof as codigo_professor,
       p.Nom_Prof as nome_professor,
       COUNT(f.pfk_Cod_Prof) as total_feedbacks,
       COALESCE(AVG(f.Qual), 0) as media_qualidade,
       COALESCE(AVG(f.Nvl_Dif), 0) as media_dificuldade
FROM Prof p
LEFT JOIN Fdbk f ON p.Cod_Prof = f.pfk_Cod_Prof
GROUP BY p.Cod_Prof, p.Nom_Prof
ORDER BY p.Nom_Prof;

-- View para feedbacks de professor específico
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
JOIN Prof p ON f.pfk_Cod_Prof = p.Cod_Prof;

-- View para médias de professor
CREATE VIEW IF NOT EXISTS view_medias_professor AS
SELECT f.pfk_Cod_Prof as professor_id,
       p.Nom_Prof as nome_professor,
       AVG(f.Qual) as media_qualidade,
       AVG(f.Nvl_Dif) as media_dificuldade,
       COUNT(*) as total_feedbacks
FROM Fdbk f
JOIN Prof p ON f.pfk_Cod_Prof = p.Cod_Prof
GROUP BY f.pfk_Cod_Prof, p.Nom_Prof;

-- View para feedbacks por turma
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
JOIN Dis d ON t.fk_Cod_Dis = d.Cod_Dis;