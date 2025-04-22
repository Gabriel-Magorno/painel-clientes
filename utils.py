from datetime import datetime

def calcular_duracao(inicio, fim):
    formato = "%Y-%m-%d"
    data_inicio = datetime.strptime(inicio, formato)
    data_fim = datetime.strptime(fim, formato)
    delta = data_fim - data_inicio
    return delta.days