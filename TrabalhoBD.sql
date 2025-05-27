CREATE DATABASE avaliacao_professores;

USE avaliacao_professores;

CREATE TABLE Dis (
    Cod_Dis VARCHAR(10) PRIMARY KEY,
    Nom_Dis VARCHAR(25),
    fk_Cod_Dep VARCHAR(10),
    Prog_Dis BLOB
);

CREATE TABLE Dep (
    Cod_Dep VARCHAR(10) PRIMARY KEY,
    Nom_Dep VARCHAR(25)
);

CREATE TABLE Tur (
    Num_Idf_Tur SMALLINT PRIMARY KEY,
    fk_Cod_Dis VARCHAR(10),
    fk_Cod_Per VARCHAR(10)
);

CREATE TABLE Prof (
    Cod_Prof SMALLINT PRIMARY KEY,
    Nom_Prof VARCHAR(25)
);

CREATE TABLE Crit_Aval_Tur (
    Num_Idf_Aval INT PRIMARY KEY,
    fk_Num_Idf_Tur SMALLINT,
    fk_Cod_Tp_Aval SMALLINT
);

CREATE TABLE Tp_Aval (
    Cod_Tp_Aval SMALLINT PRIMARY KEY,
    Nom_Tp_Aval VARCHAR(25)
);

CREATE TABLE Doc_Aval (
    Num_Idf_Doc INT PRIMARY KEY,
    Arq_Doc BLOB,
    fk_Num_Idf_Aval INT
);

CREATE TABLE Per_Let (
    Cod_Per VARCHAR(10) PRIMARY KEY,
    Ano_Per SMALLINT,
    Seq_Per SMALLINT
);

CREATE TABLE Usr (
    Num_Idf_Usr INT PRIMARY KEY,
    Nom_Usr VARCHAR(25),
    Email_Usr VARCHAR(35),
    Tel_Usr VARCHAR(20),
    Mat_Usr VARCHAR(20),
    fk_Cod_Tp_Usr SMALLINT
);

CREATE TABLE Tp_Usr (
    Cod_Tp_Usr SMALLINT PRIMARY KEY,
    Nom_Tp_Usr VARCHAR(25)
);

CREATE TABLE Fdbk (
    pfk_Num_Idf_Tur SMALLINT,
    pfk_Cod_Prof SMALLINT,
    pfk_Num_Idf_Usr INT,
    Nvl_Dif SMALLINT,
    Qual SMALLINT,
    Coment VARCHAR(100),
    PRIMARY KEY (pfk_Num_Idf_Tur, pfk_Cod_Prof, pfk_Num_Idf_Usr)
);

ALTER TABLE Dis ADD CONSTRAINT FK_Dis_Dep
    FOREIGN KEY (fk_Cod_Dep)
    REFERENCES Dep (Cod_Dep)
    ON DELETE CASCADE;

ALTER TABLE Tur ADD CONSTRAINT FK_Tur_Dis
    FOREIGN KEY (fk_Cod_Dis)
    REFERENCES Dis (Cod_Dis)
    ON DELETE CASCADE;

ALTER TABLE Tur ADD CONSTRAINT FK_Tur_Per
    FOREIGN KEY (fk_Cod_Per)
    REFERENCES Per_Let (Cod_Per)
    ON DELETE CASCADE;

ALTER TABLE Crit_Aval_Tur ADD CONSTRAINT FK_Crit_Aval_Tur_Tur
    FOREIGN KEY (fk_Num_Idf_Tur)
    REFERENCES Tur (Num_Idf_Tur)
    ON DELETE CASCADE;

ALTER TABLE Crit_Aval_Tur ADD CONSTRAINT FK_Crit_Aval_Tur_TpAval
    FOREIGN KEY (fk_Cod_Tp_Aval)
    REFERENCES Tp_Aval (Cod_Tp_Aval)
    ON DELETE CASCADE;

ALTER TABLE Doc_Aval ADD CONSTRAINT FK_Doc_Aval_CritAval
    FOREIGN KEY (fk_Num_Idf_Aval)
    REFERENCES Crit_Aval_Tur (Num_Idf_Aval)
    ON DELETE CASCADE;

ALTER TABLE Usr ADD CONSTRAINT FK_Usr_TpUsr
    FOREIGN KEY (fk_Cod_Tp_Usr)
    REFERENCES Tp_Usr (Cod_Tp_Usr)
    ON DELETE CASCADE;

ALTER TABLE Fdbk ADD CONSTRAINT FK_Fdbk_Tur
    FOREIGN KEY (pfk_Num_Idf_Tur)
    REFERENCES Tur (Num_Idf_Tur)
    ON DELETE CASCADE;

ALTER TABLE Fdbk ADD CONSTRAINT FK_Fdbk_Prof
    FOREIGN KEY (pfk_Cod_Prof)
    REFERENCES Prof (Cod_Prof)
    ON DELETE CASCADE;

ALTER TABLE Fdbk ADD CONSTRAINT FK_Fdbk_Usr
    FOREIGN KEY (pfk_Num_Idf_Usr)
    REFERENCES Usr (Num_Idf_Usr)
    ON DELETE CASCADE;