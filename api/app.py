import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from config_db import db, caminho_db
import sqlite3
from modelo import Despesa
from datetime import datetime
from tipo_pagamento_enum import TipoPagamento


app = Flask(__name__) # Inicializa o framework na variável app

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Retorna as modificações da tabela
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+caminho_db # Caminho do db
db.init_app(app)
with app.app_context():
        db.create_all()


# Listar
@app.route("/api/despesas", methods=["GET"])
def listar_despesas():
    try:
        # Armazena e formata o mês corrente na varíavel
        mes_corrente = datetime.now().strftime('%m')

        # Formata a data numérica da tabela para um formato padrão na query e filtra
        despesas = Despesa.query.filter(
            db.func.strftime('%m', db.func.date(Despesa.data)) == mes_corrente
        ).all()
        
        # Percorre todos os objetos filtrados e formata para json
        despesas_json = [despesa.to_json() for despesa in despesas]
        return criar_response(200, "data", despesas_json, True)
    except Exception as e:
        print("Erro:", e)
        return criar_response(400, "data", {"Erro": e}, False)
    
    
# Cadastrar
@app.route("/api/despesas", methods=["POST"])
def cadastrar_depesa():
    body = request.get_json()

    # Valida se nenhum dos campos está vazio
    campos = ["valor", "descricao", "data", "tipo_pagamento", "categoria"]
    campos_vazios = [campo for campo in campos if campo not in body]
    if campos_vazios:
        return criar_response(400, "data", {"Erro": f"Campos vazios: {', '.join(campos_vazios)}"}, False)

    try: 
        # Converte a string da data para um objeto de data Python
        data = datetime.strptime(body["data"], '%Y-%m-%d').date()

        # Valida o membro do Enum pelo nome, conforme syntax de Enum do Python
        tipo_pagamento_nome = body["tipo_pagamento"]
        tipo_pagamento_membro_enum = TipoPagamento[tipo_pagamento_nome]

        # Cria nova despesa da classe Despesa passando os atributos como parâmetro
        despesa = Despesa(
            valor=body["valor"],
            descricao=body["descricao"],
            data=data, # Usa a data parseada como objeto Python
            tipo_pagamento=tipo_pagamento_membro_enum,  # Usa o membro validado para o enum
            categoria=body["categoria"]
        )

        db.session.add(despesa)  # Adiciona o novo objeto através do ORM
        db.session.commit()  # Comita na tabela
        return criar_response(201, "data", despesa.id, True)
    except KeyError:
        return criar_response(400, "data", {"Erro": "Tipo de pagamento não informado ou inválido."}, False)
    except Exception as e:
        print("Erro:", e)
        return criar_response(400, "data", {"Erro": e}, False)
    
# Modulariza o padrão de response
def criar_response(status, nome_conteudo, conteudo, success):
    body = {}
    body[nome_conteudo] = conteudo
    body["success"] = success
    
    return Response(json.dumps(body), status=status, mimetype="application/json")


if __name__ == '__main__': #Inicializa a aplicação
    app.run(debug=True)
