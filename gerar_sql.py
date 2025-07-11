from main import app, db
from sqlalchemy.schema import CreateTable


# Importe todos os seus modelos aqui
from models import *

# Gere o SQL dentro do contexto da aplicação
with app.app_context():
    for table in db.metadata.sorted_tables:
        ddl = str(CreateTable(table).compile(dialect=db.engine.dialect))
        print(ddl + ';')
