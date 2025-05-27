# AvaliaUNB
## Esquema de Banco de Dados para Avaliação de Professores

Este documento contém o banco de dados em MySql chamado "avaliacao_professores", o qual será responsável por armazenar dados sobre os professores, alunos, turmas. Além disso, ele armazenará avaliações sobre a experiência dos alunos para com as aulas do semestre. 

### Tabelas

O banco de dados contém as seguintes tabelas:

* **`Dis`**: Informações sobre as disciplinas.
* **`Dep`**: Informações sobre os departamentos.
* **`Tur`**: Informações sobre as turmas.
* **`Prof`**: Informações sobre os professores.
* **`Crit_Aval_Tur`**: Critérios de avaliação para cada turma.
* **`Tp_Aval`**: Tipos de avaliação.
* **`Doc_Aval`**: Documentos de avaliação.
* **`Per_Let`**: Períodos letivos.
* **`Usr`**: Informações sobre os usuários do sistema.
* **`Tp_Usr`**: Tipos de usuários.
* **`Fdbk`**: Feedback dos usuários sobre as turmas e professores.
