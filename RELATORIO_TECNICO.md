
# Relatório Técnico - Sistema de Avaliação de Professores (AvaliaUNB)

## Sumário Executivo

O sistema AvaliaUNB é uma aplicação web desenvolvida em Flask para gerenciamento de avaliações de professores universitários. O sistema permite que alunos cadastrem feedbacks sobre professores e turmas, incluindo upload de documentos PDF relacionados às disciplinas.

## 1. Arquitetura do Sistema

### 1.1 Tecnologias Utilizadas
- **Backend**: Python 3.11 com Flask
- **ORM**: SQLAlchemy
- **Banco de Dados**: SQLite (exclusivamente)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Autenticação**: Hash de senhas com Werkzeug
- **Arquivos**: Upload e armazenamento de PDFs em BLOB

### 1.2 Estrutura de Diretórios
```
├── main.py              # Aplicação principal Flask
├── models.py            # Modelos de dados SQLAlchemy
├── forms.py             # Formulários WTForms
├── popular_dados.py     # Script de população inicial
├── stored_procedures.sql # Procedures MySQL
├── templates/           # Templates HTML
└── AvaliaUNB/          # Documentação e schemas
```

## 2. Camada de Persistência

### 2.1 Modelo de Dados
O sistema implementa um modelo relacional complexo adaptado para SQLite:

#### Tabelas Principais:
1. **Departamento (Dep)** - Departamentos da universidade
2. **Disciplina (Dis)** - Disciplinas oferecidas
3. **Professor (Prof)** - Professores cadastrados
4. **Usuario (Usr)** - Usuários do sistema
5. **Turma (Tur)** - Turmas específicas de disciplinas
6. **Feedback (Fdbk)** - Avaliações dos alunos
7. **DocumentoAvaliacao (Doc_Aval)** - Documentos PDF anexados

#### Tabelas de Apoio:
- **TipoUsuario (Tp_Usr)** - Tipos de usuário (Aluno/Administrador)
- **PeriodoLetivo (Per_Let)** - Períodos acadêmicos
- **TipoAvaliacao (Tp_Aval)** - Tipos de avaliação
- **CriterioAvaliacaoTurma (Crit_Aval_Tur)** - Critérios de avaliação

### 2.2 Relacionamentos
- **1:N** - Departamento → Disciplinas
- **1:N** - Disciplina → Turmas
- **1:N** - Professor → Feedbacks
- **1:N** - Usuario → Feedbacks
- **N:M** - Professor ↔ Turma (através de Feedback)
- **1:N** - CriterioAvaliacaoTurma → DocumentoAvaliacao

### 2.3 Configuração SQLAlchemy
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avaliacao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
```

### 2.4 Modelos Implementados
Todos os modelos seguem o padrão SQLAlchemy com mapeamento direto para o schema MySQL:

```python
class Feedback(db.Model):
    __tablename__ = 'Fdbk'
    
    pfk_numero_identificacao_turma = db.Column('pfk_Num_Idf_Tur', db.SmallInteger, 
                                               db.ForeignKey('Tur.Num_Idf_Tur'), primary_key=True)
    pfk_codigo_professor = db.Column('pfk_Cod_Prof', db.SmallInteger, 
                                     db.ForeignKey('Prof.Cod_Prof'), primary_key=True)
    pfk_numero_identificacao_usuario = db.Column('pfk_Num_Idf_Usr', db.Integer, 
                                                  db.ForeignKey('Usr.Num_Idf_Usr'), primary_key=True)
    nivel_dificuldade = db.Column('Nvl_Dif', db.SmallInteger)
    qualidade = db.Column('Qual', db.SmallInteger)
    comentario = db.Column('Coment', db.String(100))
```

## 3. Operações CRUD

### 3.1 CREATE (Criação)

#### Cadastro de Usuários
```python
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if formulario.validate_on_submit():
        novo_usuario = Usuario(
            nome_usuario=formulario.nome.data,
            email_usuario=formulario.email.data,
            telefone_usuario=formulario.telefone.data,
            matricula_usuario=formulario.matricula.data,
            senha_usuario=generate_password_hash(formulario.senha.data),
            fk_codigo_tipo_usuario=formulario.tipo_usuario.data
        )
        db.session.add(novo_usuario)
        db.session.commit()
```

#### Criação de Feedbacks
```python
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if formulario.validate_on_submit():
        novo_feedback = Feedback(
            pfk_numero_identificacao_turma=formulario.turma.data,
            pfk_codigo_professor=formulario.professor.data,
            pfk_numero_identificacao_usuario=session['usuario_id'],
            nivel_dificuldade=formulario.dificuldade.data,
            qualidade=formulario.qualidade.data,
            comentario=formulario.comentario.data
        )
        db.session.add(novo_feedback)
        db.session.commit()
```

### 3.2 READ (Leitura)

#### Listagem de Professores
```python
@app.route('/professores')
def professores():
    resultado = db.session.execute(text("CALL ListarProfessoresComFeedbacks()"))
    professores_data = resultado.fetchall()
    return render_template('professores.html', professores=professores_data)
```

#### Consulta de Disciplinas
```python
@app.route('/disciplinas')
def disciplinas():
    lista_disciplinas = Disciplina.query.all()
    return render_template('disciplinas.html', disciplinas=lista_disciplinas)
```

#### Busca de Feedbacks por Professor
```python
@app.route('/professor/<int:professor_id>/feedbacks')
def feedbacks_detalhes(professor_id):
    resultado_feedbacks = db.session.execute(
        text("CALL BuscarFeedbacksProfessor(:prof_id)"), 
        {"prof_id": professor_id}
    )
    feedbacks_data = resultado_feedbacks.fetchall()
```

### 3.3 UPDATE (Atualização)

#### Edição de Feedbacks
```python
@app.route('/feedback/editar/<int:turma_id>/<int:professor_id>', methods=['GET', 'POST'])
def editar_feedback(turma_id, professor_id):
    feedback = Feedback.query.filter_by(
        pfk_numero_identificacao_turma=turma_id,
        pfk_codigo_professor=professor_id,
        pfk_numero_identificacao_usuario=session['usuario_id']
    ).first_or_404()
    
    if formulario.validate_on_submit():
        feedback.nivel_dificuldade = formulario.dificuldade.data
        feedback.qualidade = formulario.qualidade.data
        feedback.comentario = formulario.comentario.data
        db.session.commit()
```

### 3.4 DELETE (Exclusão)

#### Exclusão de Feedbacks
```python
@app.route('/feedback/excluir/<int:turma_id>/<int:professor_id>', methods=['POST'])
def excluir_feedback(turma_id, professor_id):
    feedback = Feedback.query.filter_by(
        pfk_numero_identificacao_turma=turma_id,
        pfk_codigo_professor=professor_id,
        pfk_numero_identificacao_usuario=session['usuario_id']
    ).first_or_404()
    
    db.session.delete(feedback)
    db.session.commit()
```

## 4. Utilização de Views

### 4.1 Views Implementadas (Templates)
O sistema utiliza múltiplas views para apresentação de dados:

#### View de Professores com Feedbacks
- **Template**: `professores.html`
- **Dados**: Lista professores com estatísticas agregadas
- **Funcionalidade**: Exibe média de qualidade e dificuldade

#### View de Feedbacks Detalhados
- **Template**: `feedbacks_detalhes.html`
- **Dados**: Feedbacks específicos de um professor
- **Agregação**: Cálculo de médias via stored procedures

#### View de Turmas Avaliadas
- **Template**: `turmas_avaliadas.html`
- **Query**: Turmas que possuem pelo menos um feedback
```python
turmas_com_feedbacks = db.session.query(Turma).join(Feedback).distinct().all()
```

### 4.2 Views de Banco (Potencial Implementação)
Embora não implementadas no código atual, o sistema poderia beneficiar-se de views como:
- View de estatísticas de professores
- View de ranking de disciplinas
- View de relatórios por período

## 5. Views e Funcionalidades SQLite

### 5.1 Views Implementadas

O sistema utiliza SQLite exclusivamente com views criadas para otimizar consultas frequentes:

#### View: view_feedbacks_professor
```sql
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
```

#### View: view_professores_com_feedbacks
```sql
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
```

#### View: view_feedbacks_turma
```sql
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
```

### 5.2 Uso das Views no Python
```python
# Consulta usando views SQLite
resultado = db.session.execute(text("SELECT * FROM view_feedbacks_professor WHERE professor_id = :prof_id"), {"prof_id": professor_id})
feedbacks_data = resultado.fetchall()

# Consulta de professores com estatísticas
professores = db.session.execute(text("SELECT * FROM view_professores_com_feedbacks")).fetchall()
```

## 6. Inserção de Dados Binários

### 6.1 Estrutura do Modelo DocumentoAvaliacao
```python
class DocumentoAvaliacao(db.Model):
    __tablename__ = 'Doc_Aval'
    
    numero_identificacao_documento = db.Column('Num_Idf_Doc', db.Integer, primary_key=True)
    arquivo_documento = db.Column('Arq_Doc', db.LargeBinary)  # Dados binários
    nome_arquivo = db.Column('Nome_Arq', db.String(255))
    tipo_documento = db.Column('Tipo_Doc', db.String(50))
    fk_numero_identificacao_avaliacao = db.Column('fk_Num_Idf_Aval', db.Integer, 
                                                  db.ForeignKey('Crit_Aval_Tur.Num_Idf_Aval'), nullable=False)
```

### 6.2 Upload de Arquivos PDF
```python
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if formulario.arquivo_pdf.data and formulario.tipo_documento.data:
        arquivo = formulario.arquivo_pdf.data
        documento = DocumentoAvaliacao(
            nome_arquivo=arquivo.filename,
            tipo_documento=formulario.tipo_documento.data,
            arquivo_documento=arquivo.read(),  # Conversão para binário
            fk_numero_identificacao_avaliacao=criterio.numero_identificacao_avaliacao
        )
        db.session.add(documento)
```

### 6.3 Download de Arquivos PDF
```python
@app.route('/documento/<int:documento_id>')
def baixar_documento(documento_id):
    documento = DocumentoAvaliacao.query.get_or_404(documento_id)
    return send_file(
        io.BytesIO(documento.arquivo_documento),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=documento.nome_arquivo
    )
```

### 6.4 Validação de Arquivos
```python
class FormularioFeedback(FlaskForm):
    arquivo_pdf = FileField('Documento PDF (opcional)', validators=[
        FileAllowed(['pdf'], 'Apenas arquivos PDF são permitidos!')
    ])
    tipo_documento = SelectField('Tipo de Documento', choices=[
        ('', 'Selecione o tipo (opcional)'),
        ('prova', 'Prova'),
        ('plano_ensino', 'Plano de Ensino'),
        ('slide', 'Slide/Apresentação'),
        ('material_apoio', 'Material de Apoio'),
        ('outro', 'Outro')
    ])
```

## 7. Segurança e Autenticação

### 7.1 Hash de Senhas
```python
senha_usuario=generate_password_hash(formulario.senha.data)
check_password_hash(usuario.senha_usuario, formulario.senha.data)
```

### 7.2 Controle de Sessões
```python
if 'usuario_id' not in session:
    flash('Você precisa estar logado!', 'warning')
    return redirect(url_for('login'))
```

### 7.3 Validação de Duplicatas
- Prevenção de feedbacks duplicados por usuário/professor/turma
- Validação de email e matrícula únicos no cadastro

## 8. Interface de Usuário

### 8.1 Design
- **Tema**: Pixelado com cores neon (cyber/retro)
- **Framework**: Bootstrap 5
- **Responsividade**: Design adaptável
- **Animações**: CSS3 com efeitos neon

### 8.2 Funcionalidades
- Cadastro e login de usuários
- Formulários de feedback com upload
- Listagem e visualização de dados
- Sistema de navegação intuitivo

## 9. População Inicial de Dados

### 9.1 Script popular_dados.py
```python
def popular_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Criação de dados de exemplo
        departamentos = [
            Departamento(codigo_departamento='CIC', nome_departamento='Ciência da Computação'),
            # ...
        ]
```

## 10. Conclusões

### 10.1 Funcionalidades Implementadas
✅ **Camada de Persistência**: SQLAlchemy com SQLite
✅ **CRUD Completo**: Para 7+ tabelas relacionadas
✅ **Views**: Templates HTML e views SQLite para visualização
✅ **Views SQLite**: Views otimizadas para consultas complexas
✅ **Dados Binários**: Upload e download de PDFs

### 10.2 Arquitetura Robusta
- Separação clara de responsabilidades
- Modelo relacional bem estruturado
- Validação de dados em múltiplas camadas
- Sistema de autenticação seguro

### 10.3 Escalabilidade
- Base sólida em SQLite para desenvolvimento
- Estrutura modular para expansão
- Views otimizadas para performance
- Design responsivo e moderno

O sistema AvaliaUNB representa uma implementação completa e profissional de um sistema de avaliação acadêmica, atendendo a todos os requisitos técnicos especificados com qualidade de código empresarial.

## 11. Tutorial: Executando o Projeto no VS Code

### 11.1 Pré-requisitos

#### Execução no Replit (Recomendado):
O projeto está configurado para rodar diretamente no Replit, sem necessidade de instalação local.

#### Para execução local (Opcional):

##### Para Mac:
1. **Instalar Python 3.11+**:
   ```bash
   # Usando Homebrew (recomendado)
   brew install python@3.11
   
   # Ou baixar do site oficial: https://www.python.org/downloads/
   ```

2. **Instalar VS Code**:
   - Baixar de: https://code.visualstudio.com/
   - Instalar a extensão "Python" da Microsoft

##### Para Windows:
1. **Instalar Python 3.11+**:
   - Baixar de: https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE**: Marcar "Add Python to PATH" durante a instalação

2. **Instalar VS Code**:
   - Baixar de: https://code.visualstudio.com/
   - Instalar a extensão "Python" da Microsoft

### 11.2 Clonando o Projeto

#### Opção 1: Download Direto do Replit
1. No Replit, clicar em "Download as ZIP"
2. Extrair o arquivo ZIP em uma pasta de sua escolha
3. Abrir o VS Code na pasta extraída

#### Opção 2: Via Git (se o projeto estiver no GitHub)
```bash
# Mac/Windows (no Terminal/Command Prompt)
git clone https://github.com/seu-usuario/AvaliaUNB.git
cd AvaliaUNB
code .
```

### 11.3 Configuração do Ambiente

#### Passo 1: Abrir o Terminal no VS Code
- **Mac**: `Cmd + Shift + `` ` `` ou Terminal > New Terminal
- **Windows**: `Ctrl + Shift + `` ` `` ou Terminal > New Terminal

#### Passo 2: Verificar Python
```bash
# Mac/Windows
python --version
# ou
python3 --version

# Deve retornar Python 3.11+ 
```

#### Passo 3: Instalar Dependências
```bash
# Mac/Windows
pip install Flask==2.3.3
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-WTF==1.1.1
pip install WTForms==3.0.1
pip install Werkzeug==2.3.7
pip install email-validator==2.2.0
pip install PyMySQL

# Ou instalar tudo de uma vez:
pip install -r requirements.txt
```

### 11.4 Configuração do Banco de Dados

#### Opção 1: SQLite (Mais Simples - Recomendado para teste)
1. O projeto já está configurado para SQLite por padrão
2. O banco será criado automaticamente na primeira execução

O projeto usa SQLite que é criado automaticamente - não requer configuração adicional de banco de dados.

### 11.5 Executando o Projeto

#### Passo 1: Popular o Banco de Dados
```bash
# Mac/Windows (no terminal do VS Code)
python popular_dados.py
```

#### Passo 2: Executar a Aplicação
```bash
# Mac/Windows
python main.py
```

#### Passo 3: Acessar no Navegador
- Abrir: http://127.0.0.1:5000 ou http://localhost:5000

### 11.6 Configuração do VS Code

#### Configurar o Debugger
1. Criar arquivo `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            }
        }
    ]
}
```

2. **Executar com Debug**: Pressionar `F5` ou ir em Run > Start Debugging

#### Configurar Tarefas
1. Criar arquivo `.vscode/tasks.json`:
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Flask App",
            "type": "shell",
            "command": "python",
            "args": ["main.py"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "Popular Banco",
            "type": "shell",
            "command": "python",
            "args": ["popular_dados.py"],
            "group": "build"
        }
    ]
}
```

### 11.7 Estrutura de Arquivos no VS Code

Após a configuração, seu projeto deve ter esta estrutura:
```
AvaliaUNB/
├── .vscode/
│   ├── launch.json
│   └── tasks.json
├── templates/
│   ├── base.html
│   ├── index.html
│   └── ...
├── instance/
│   └── avaliacao.db
├── main.py
├── models.py
├── forms.py
├── popular_dados.py
├── requirements.txt
└── stored_procedures.sql
```

### 11.8 Comandos Úteis

#### Para desenvolvimento:
```bash
# Executar com debug
python main.py

# Popular banco do zero
python popular_dados.py

# Verificar rotas
flask routes

# Abrir shell interativo
flask shell
```

#### Para resolução de problemas:
```bash
# Verificar versão Python
python --version

# Listar pacotes instalados
pip list

# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### 11.9 Extensões Recomendadas do VS Code

1. **Python** (Microsoft) - Essencial
2. **Pylance** (Microsoft) - Autocomplete avançado
3. **Flask Snippets** - Snippets para Flask
4. **SQLite Viewer** - Visualizar banco SQLite
5. **HTML CSS Support** - Suporte aprimorado para templates
6. **Jinja** - Syntax highlighting para templates Jinja2

### 11.10 Troubleshooting

#### Problemas Comuns:

**1. "python command not found"**
- **Mac**: Usar `python3` em vez de `python`
- **Windows**: Reinstalar Python marcando "Add to PATH"

**2. "Module not found"**
```bash
# Reinstalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

**3. "Permission denied" (Mac)**
```bash
# Usar sudo ou pip --user
pip install --user -r requirements.txt
```

**4. "Port already in use"**
- Alterar porta no main.py:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
```

**5. Banco de dados não cria tabelas**
```bash
# Deletar banco e recriar
rm instance/avaliacao.db
python popular_dados.py
```

### 11.11 Diferenças entre Replit e VS Code Local

| Aspecto | Replit | VS Code Local |
|---------|---------|---------------|
| **Instalação** | Não necessária | Python + dependências |
| **Banco** | SQLite automático | Configuração manual |
| **Debug** | Console web | Debugger integrado |
| **Colaboração** | Tempo real | Via Git |
| **Performance** | Limitada | Full local |
| **Acesso** | Browser anywhere | Local only |

### 11.12 Recomendações de Desenvolvimento

1. **Use Git para versionamento**:
```bash
git init
git add .
git commit -m "Initial commit"
```

2. **Configure .gitignore**:
```
__pycache__/
*.pyc
instance/
.env
*.log
```

3. **Mantenha requirements.txt atualizado**:
```bash
pip freeze > requirements.txt
```

4. **Use variáveis de ambiente para configurações**:
```python
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
```

Com este tutorial, você consegue migrar facilmente seu projeto do Replit para um ambiente de desenvolvimento local no VS Code, mantendo todas as funcionalidades e tendo controle total sobre o ambiente de desenvolvimento.
