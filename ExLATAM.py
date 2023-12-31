from AnaliseDados import Extrair
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.webdriver import *
import re
import json

estados = [
    "São Paulo, SAO - Brasil",
    "Belém, BEL - Brasil",
    "Rio Branco, RBR - Brasil",
    "São Luís, SLZ - Brasil",
    "Fortaleza, FOR - Brasil",
    "Recife, REC - Brasil",
    "Aracaju, AJU - Brasil",
    "Salvador da Bahia, SSA - Brasil",
    "Belo Horizonte, BHZ - Brasil",
    "Vitória, VIX - Brasil",
    "Rio de Janeiro, RIO - Brasil",
    "Curitiba, CWB - Brasil",
    "Porto Alegre, POA - Brasil",
    "Goiânia, GYN - Brasil",
    "Brasília, BSB - Brasil"
]

siglas = [
    "SAO",
    "BEL",
    "RBR",
    "SLZ",
    "FOR",
    "REC",
    "AJU",
    "SSA",
    "BHZ",
    "VIX",
    "RIO",
    "CWB",
    "POA",
    "GYN",
    "BSB"
]

timeGap = 0.5
timeWait = 10


class ExLATAM(Extrair):
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

# Reinicia o driver para que os passos sejam iguais todas as vezes, porque a mensagem de cookies só aparece uma única vez ao abrir um driver e sempre que uma busca era feita, uma nova aba era criada. Essa decsão reduziu o meu trabalho.
    def restart(self):
        self.driver.close()
        self.__init__()

# Descreve os passos para remover o popup dos cookies
    def avoidCookiePopUp(self):
        time.sleep(timeGap)
        element = self.driver.find_element(
            By.ID, "cookies-politics-button")
        element.click()
        time.sleep(timeGap)

# Descreve os passos para realizar uma busca e troca de tab no navegador
    def getUrl(self, origem, destino):
        self.driver.get("https://www.latamairlines.com/br/pt")

        self.driver.maximize_window()

        self.avoidCookiePopUp()

        # Set origin

        self.driver.find_element(
            By.ID, "txtInputOrigin_field").send_keys(origem)

        self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/ul/li/button").click()

        time.sleep(timeGap)

        # Set destination

        self.driver.find_element(
            By.ID, "txtInputDestination_field").send_keys(destino)

        self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/ul/li/button").click()

        # Set Departure Date

        self.driver.find_element(
            By.ID, "departureDate").click()

        time.sleep(timeGap)

        self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[6]").click()

        self.driver.find_element(
            By.ID, "departureDate").send_keys("sáb.. 26 de ago.")

        # Set Arrival Date

        time.sleep(timeGap)

        self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[4]/td[7]").click()

        self.driver.find_element(
            By.ID, "arrivalDate").send_keys("dom.. 27 de ago.")

        # Hit search button

        time.sleep(timeGap)
        self.driver.find_element(By.ID, "btnSearchCTA").click()

        # Change to new window

        original_window = self.driver.current_window_handle
        WebDriverWait(self.driver, timeWait).until(
            EC.number_of_windows_to_be(2))
        for window in self.driver.window_handles:
            if window != original_window:
                self.driver.switch_to.window(window)
                break

# Espera a página carregar por timeWait segundos. Essa é uma variável global
    def getPageSource(self):
        WebDriverWait(self.driver, timeWait).until(
            EC.presence_of_element_located((By.ID, "WrapperCardFlight0")))

# Dada uma página com horários e valores, extrai todos os dados que estamos interessados e os limpa usando expressões regulares
    def getData(self):
        source = bs(self.driver.page_source, "html.parser")
        parent = source.find('ol')
        childs = parent.find_all(
            'li', class_='body-flightsstyle__ListItemAvailableFlights-sc__sc-1p74not-5 ixybDA')
        value = []
        for child in childs:
            span = child.find('span')
            h = re.search("(([0-1]?[0-9]|2[0-3]):[0-5][0-9])", span.text)
            p = re.search("(\d*\.\d+\,\d{1,2})|(\d+,\d{1,2})", span.text)
            value.append([h.group(), p.group()])
        return value

# Faz a chamada dos métodos com try-catchs e armazena os dados em arquivos .json. Note que essa função faz esse processo de 15*14 vezes.
    def scrape(self):
        """Retira os dados no contexto da LATAM"""
        data = []
        for i, origem in enumerate(estados):
            for j, destino in enumerate(estados):
                if origem != destino:
                    self.restart()
                    row = {}
                    row["origin"] = siglas[i]
                    row["destination"] = siglas[j]
                    try:
                        self.getUrl(estados[i], estados[j])
                    except:
                        print(
                            f" [-] Erro em getUrl: {estados[i]} e {estados[j]}")
                    try:
                        self.getPageSource()
                    except:
                        print(
                            f" [-] Erro em getPageSource: {estados[i]} e {estados[j]}")
                    try:
                        row['value'] = self.getData()
                    except:
                        print(
                            f" [-] Erro em getData: {estados[i]} e {estados[j]}")
                        row['value'] = []
                    print(row)
                    data.append(row)
                    time.sleep(timeGap)
        # print("--------------")
        # print(data)
        df = json.dumps(data)
        f = open("LATAM.json", "w")
        f.write(df)
        f.close()


x = ExLATAM()
x.scrape()
