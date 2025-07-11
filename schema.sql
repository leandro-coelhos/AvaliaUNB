CREATE TABLE "Dep" (
        "Cod_Dep" VARCHAR(10) NOT NULL,
        "Nom_Dep" VARCHAR(25),
        PRIMARY KEY ("Cod_Dep")
)

;

CREATE TABLE "Per_Let" (
        "Cod_Per" INTEGER NOT NULL,
        "Ano_Per" SMALLINT,
        "Seq_Per" SMALLINT,
        PRIMARY KEY ("Cod_Per")
)

;

CREATE TABLE "Prof" (
        "Cod_Prof" SMALLINT NOT NULL,
        "Nom_Prof" VARCHAR(25),
        PRIMARY KEY ("Cod_Prof")
)

;

CREATE TABLE "Tp_Aval" (
        "Cod_Tp_Aval" SMALLINT NOT NULL,
        "Nom_Tp_Aval" VARCHAR(25),
        PRIMARY KEY ("Cod_Tp_Aval")
)

;

CREATE TABLE "Tp_Usr" (
        "Cod_Tp_Usr" SMALLINT NOT NULL,
        "Nom_Tp_Usr" VARCHAR(25),
        PRIMARY KEY ("Cod_Tp_Usr")
)

;

CREATE TABLE "Dis" (
        "Cod_Dis" VARCHAR(10) NOT NULL,
        "Nom_Dis" VARCHAR(25),
        "fk_Cod_Dep" VARCHAR(10) NOT NULL,
        "Prog_Dis" BLOB,
        PRIMARY KEY ("Cod_Dis"),
        FOREIGN KEY("fk_Cod_Dep") REFERENCES "Dep" ("Cod_Dep")
)

;

CREATE TABLE "Usr" (
        "Num_Idf_Usr" INTEGER NOT NULL,
        "Nom_Usr" VARCHAR(25),
        "Email_Usr" VARCHAR(35),
        "Tel_Usr" VARCHAR(20),
        "Mat_Usr" VARCHAR(20),
        "Senha_Usr" VARCHAR(255),
        "fk_Cod_Tp_Usr" SMALLINT NOT NULL,
        PRIMARY KEY ("Num_Idf_Usr"),
        FOREIGN KEY("fk_Cod_Tp_Usr") REFERENCES "Tp_Usr" ("Cod_Tp_Usr")
)

;

CREATE TABLE "Tur" (
        "Num_Idf_Tur" SMALLINT NOT NULL,
        "fk_Cod_Dis" VARCHAR(10) NOT NULL,
        "fk_Cod_Per" VARCHAR(10) NOT NULL,
        "fk_Cod_Prof" SMALLINT,
        PRIMARY KEY ("Num_Idf_Tur"),
        FOREIGN KEY("fk_Cod_Dis") REFERENCES "Dis" ("Cod_Dis"),
        FOREIGN KEY("fk_Cod_Per") REFERENCES "Per_Let" ("Cod_Per"),
        FOREIGN KEY("fk_Cod_Prof") REFERENCES "Prof" ("Cod_Prof")
)

;

CREATE TABLE "Crit_Aval_Tur" (
        "Num_Idf_Aval" INTEGER NOT NULL,
        "fk_Num_Idf_Tur" SMALLINT NOT NULL,
        "fk_Cod_Tp_Aval" SMALLINT NOT NULL,
        PRIMARY KEY ("Num_Idf_Aval"),
        FOREIGN KEY("fk_Num_Idf_Tur") REFERENCES "Tur" ("Num_Idf_Tur"),
        FOREIGN KEY("fk_Cod_Tp_Aval") REFERENCES "Tp_Aval" ("Cod_Tp_Aval")
)

;

CREATE TABLE "Fdbk" (
        "pfk_Num_Idf_Tur" SMALLINT NOT NULL,
        "pfk_Cod_Prof" SMALLINT NOT NULL,
        "pfk_Num_Idf_Usr" INTEGER NOT NULL,
        "Nvl_Dif" SMALLINT,
        "Qual" SMALLINT,
        "Coment" VARCHAR(100),
        PRIMARY KEY ("pfk_Num_Idf_Tur", "pfk_Cod_Prof", "pfk_Num_Idf_Usr"),
        FOREIGN KEY("pfk_Num_Idf_Tur") REFERENCES "Tur" ("Num_Idf_Tur"),
        FOREIGN KEY("pfk_Cod_Prof") REFERENCES "Prof" ("Cod_Prof"),
        FOREIGN KEY("pfk_Num_Idf_Usr") REFERENCES "Usr" ("Num_Idf_Usr")
)

;

CREATE TABLE "Doc_Aval" (
        "Num_Idf_Doc" INTEGER NOT NULL,
        "Arq_Doc" BLOB,
        "Nome_Arq" VARCHAR(255),
        "Tipo_Doc" VARCHAR(50),
        "fk_Num_Idf_Aval" INTEGER NOT NULL,
        "fk_Usr_Id" INTEGER,
        "fk_Prof_Id" SMALLINT,
        "fk_Tur_Id" SMALLINT,
        PRIMARY KEY ("Num_Idf_Doc"),
        FOREIGN KEY("fk_Num_Idf_Aval") REFERENCES "Crit_Aval_Tur" ("Num_Idf_Aval"),
        FOREIGN KEY("fk_Usr_Id") REFERENCES "Usr" ("Num_Idf_Usr"),
        FOREIGN KEY("fk_Prof_Id") REFERENCES "Prof" ("Cod_Prof"),
        FOREIGN KEY("fk_Tur_Id") REFERENCES "Tur" ("Num_Idf_Tur")
)

;