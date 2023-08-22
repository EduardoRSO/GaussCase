from AnaliseDados import Analisar
import json

siglas = {
    "SAO": 32.28,
    "BEL": 3.94,
    "RBR": 0.51,
    "SLZ": 1.62,
    "FOR": 3.23,
    "REC": 3.92,
    "AJU": 1.03,
    "SSA": 5.99,
    "BHZ": 9.69,
    "VIX": 1.86,
    "RIO": 9.43,
    "CWB": 8.09,
    "POA": 8.61,
    "GYN": 4.17,
    "BSB": 4.06
}


class AnLATAM(Analisar):

    def __init__(self, filename):
        with open(filename) as json_file:
            self.data = json.load(json_file)

    def getOrigin(self, index):
        frame = self.data[index]
        return frame['origin']

    def getDestination(self, index):
        frame = self.data[index]
        return frame['destination']

    def getValues(self, index):
        frame = self.data[index]
        return frame['value']

# Retorna o menor indíce em duas listas


def minIndex(x, y):
    return min(len(x), len(y))

# Como houveram dados discrepantes, optei por fazer o cálculo da variação percentual diária baseada no tamanho dos dados coletados que estejam presentes nas duas amostras. Uma possível melhoria seria assegurar que os horários também sejam iguais. No entanto, não sei como lidar com os dados que faltaram por motivos adversos(EX: viagem agora indisponível, horários diferentes, etc)

# Realiza a variação percentual diária de dois dict['value'] e retorna 0 caso não hajam pelo menos um dado em ambos.


def vpd(x, y):
    var = []
    total = minIndex(x, y)
    if total == 0:
        return 0
    soma = 0
    for index in range(0, total):
        xp = float(x[index][1].replace(",", "."))
        yp = float(y[index][1].replace(",", "."))
        soma += ((xp - yp)/yp)*100
    return soma/total

# Retorna a soma dos pesos para o cálculo da média ponderada


def getWeightSum():
    wSum = 0
    for key in siglas:
        wSum += siglas[key]
    return wSum


# Criei um dicionário do tipo <destino, vpd>.
def main():
    # uma possível melhoria seria aceitar um número arbitrário de arquivos para agregar na qualidade da análise se a extração fosse feita em vários dias ou até mesmo em várias horas distintas de vários dias.
    x = AnLATAM("LATAM22082023.json")
    y = AnLATAM("LATAM21082023.json")
    variacao = {}
    mp = 0

    # itero por todos os dados obtidos em origem-destino e calculo a variação percentual diária (vpd)
    for index in range(0, len(x.data)):
        key = x.getOrigin(index) + x.getDestination(index)
        if variacao.get(key) == None:
            variacao[key] = 0
        variacao[key] += vpd(x.getValues(index), y.getValues(index))

    # após armazenar as vpd's em dicionários do tipo <origemdestino, valor>, para o cálculo da média ponderada eu considero apenas os destinos, que podem ser obtidos por key[3:6]. O dicionário de siglas tem como valor de uma chave o peso da ponderação.
    for key in variacao.keys():
        mp += variacao[key] * siglas[key[3:6]]

    print(mp/getWeightSum())


main()
