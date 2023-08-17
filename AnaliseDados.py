class Extrair:
    def scrape() -> str:
        """Retira os dados"""
        pass


class Processar:
    def limpa() -> str:
        """Limpa os dados"""
        pass

    def insere() -> str:
        """Conecta com o BD e insere os dados"""
        pass


class BD:
    def cria(bdNome) -> str:
        """Cria um banco de dados com nome bdNome """
        pass

    def conecta(bdNome) -> str:
        """Realiza a conexão com o bd"""
        pass

    def insere(bdNome) -> str:
        """Insere o dado fornecido"""
        pass

    def consulta(consulta, bdNome) -> str:
        """Realiza a consulta fornecida no bd"""
        pass


class Analisar:

    def Modelo() -> str:
        """Aplica o modelo implementado"""
        pass


class Compartilhar:

    def le() -> str:
        """Receber os dados da analise"""
        pass

    def criaGrafico(parametros) -> str:
        """"Cria um gráfico dados os parametros"""
        pass

    def outputRelatorio() -> str:
        """"Gera o relatório no formato desejado"""
        pass
