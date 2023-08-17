class Extrair:
    def scrape(self):
        """Retira os dados"""
        pass


class ExGOL(Extrair):
    def scrape(self):
        """Retira os dados no contexto da GOL"""
        pass


class ExLATAM(Extrair):
    def scrape(self):
        """Retira os dados no contexto da LATAM"""
        pass


class ExAZUL(Extrair):
    def scrape(self):
        """Retira os dados no contexto da AZUL"""
        pass


class Processar:
    def limpa(self):
        """Limpa os dados"""
        pass

    def insere(self):
        """Conecta com o BD e insere os dados"""
        pass


class BD:
    def cria(self, fbdNome):
        """Cria um banco de dados com nome bdNome """
        pass

    def conecta(self, bdNome):
        """Realiza a conexão com o bd"""
        pass

    def insere(self, bdNome):
        """Insere o dado fornecido"""
        pass

    def consulta(self, consulta, bdNome):
        """Realiza a consulta fornecida no bd"""
        pass


class Analisar:

    def Modelo(self):
        """Aplica o modelo implementado"""
        pass


class Compartilhar:

    def le(self):
        """Receber os dados da analise"""
        pass

    def criaGrafico(self, parametros):
        """"Cria um gráfico dados os parametros"""
        pass

    def outputRelatoriop(self):
        """"Gera o relatório no formato desejado"""
        pass
