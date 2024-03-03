import random
import datetime
from dateutil import relativedelta
import string

class Utils:

    # --- Retorna quantos meses tem entre a data do último processamento e hoje ---
    def diferenca_meses(self, data):

        hoje = datetime.date.today()
        diferenca = relativedelta.relativedelta(hoje, data)
        return diferenca.months

    # --- Gera string aleatória ---
    def gerador_alfanumerico(self, tamanho=10, caracteres=string.ascii_letters + string.digits):
        
        return ''.join(random.choice(caracteres) for _ in range(tamanho))