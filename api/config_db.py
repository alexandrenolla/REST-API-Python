from flask_sqlalchemy import SQLAlchemy
import os

caminho_pasta = os.path.abspath(os.path.dirname(__file__)) # Caminho absoluto do diretório do usuário
banco_dados = 'orcamento_domestico.sqlite' # Nome do db
caminho_db = os.path.join(caminho_pasta, banco_dados) # Integra O caminho do diretório com o db

db = SQLAlchemy() # Instancia o ORM