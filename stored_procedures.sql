
USE avaliacao_professores;

DELIMITER $$

CREATE PROCEDURE BuscarFeedbacksProfessor(IN professor_id INT)
BEGIN
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
    WHERE f.pfk_Cod_Prof = professor_id
    ORDER BY t.Num_Idf_Tur;
END$$

CREATE PROCEDURE CalcularMediasProfessor(IN professor_id INT)
BEGIN
    SELECT f.pfk_Cod_Prof as professor_id,
           p.Nom_Prof as nome_professor,
           AVG(f.Qual) as media_qualidade,
           AVG(f.Nvl_Dif) as media_dificuldade,
           COUNT(*) as total_feedbacks
    FROM Fdbk f
    JOIN Prof p ON f.pfk_Cod_Prof = p.Cod_Prof
    WHERE f.pfk_Cod_Prof = professor_id
    GROUP BY f.pfk_Cod_Prof, p.Nom_Prof;
END$$

CREATE PROCEDURE ListarProfessoresComFeedbacks()
BEGIN
    SELECT p.Cod_Prof as codigo_professor,
           p.Nom_Prof as nome_professor,
           COUNT(f.pfk_Cod_Prof) as total_feedbacks,
           AVG(f.Qual) as media_qualidade,
           AVG(f.Nvl_Dif) as media_dificuldade
    FROM Prof p
    LEFT JOIN Fdbk f ON p.Cod_Prof = f.pfk_Cod_Prof
    GROUP BY p.Cod_Prof, p.Nom_Prof
    ORDER BY total_feedbacks DESC;
END$$

CREATE PROCEDURE BuscarFeedbacksPorTurma(IN turma_id INT)
BEGIN
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
    WHERE f.pfk_Num_Idf_Tur = turma_id
    ORDER BY f.Qual DESC;
END$$

CREATE PROCEDURE InserirFeedback(
    IN p_turma_id INT,
    IN p_professor_id INT,
    IN p_usuario_id INT,
    IN p_nivel_dificuldade INT,
    IN p_qualidade INT,
    IN p_comentario VARCHAR(100)
)
BEGIN
    DECLARE feedback_existe INT DEFAULT 0;
    
    SELECT COUNT(*) INTO feedback_existe
    FROM Fdbk
    WHERE pfk_Num_Idf_Tur = p_turma_id
    AND pfk_Cod_Prof = p_professor_id
    AND pfk_Num_Idf_Usr = p_usuario_id;
    
    IF feedback_existe = 0 THEN
        INSERT INTO Fdbk (pfk_Num_Idf_Tur, pfk_Cod_Prof, pfk_Num_Idf_Usr, Nvl_Dif, Qual, Coment)
        VALUES (p_turma_id, p_professor_id, p_usuario_id, p_nivel_dificuldade, p_qualidade, p_comentario);
        SELECT 'Feedback inserido com sucesso' as resultado;
    ELSE
        SELECT 'Feedback já existe para esta combinação' as resultado;
    END IF;
END$$

DELIMITER ;
