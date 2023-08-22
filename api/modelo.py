from config_db import db
from tipo_pagamento_enum import TipoPagamento


class Despesa(db.Model): # herda do SQLAlchemy
    id = db.Column(db.Integer, primary_key= True)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(80))
    data = db.Column(db.Date, nullable=False)
    tipo_pagamento = db.Column(db.Enum(TipoPagamento), nullable=False)
    categoria = db.Column(db.String(30), nullable=False)

    def to_json(self): # Método que retorna um dicionário com o JSON preparado para retornar no endpoint
        return {"id": self.id,
                "valor": self.valor,
                "descricao": self.descricao,
                "data": self.data.strftime('%Y-%m-%d'), # Converte a data para string
                "tipo_pagamento": self.tipo_pagamento.value, # Acessa o valor do enum
                "categoria": self.categoria}

