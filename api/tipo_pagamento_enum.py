from enum import Enum


class TipoPagamento(Enum):
    dinheiro = 'Dinheiro'
    debito = 'Débito'
    credito = 'Crédito'
    pix = 'Pix'

    def __str__(self):
        return self.value