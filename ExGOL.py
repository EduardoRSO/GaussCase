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
    " São Paulo  - Todos os Aeroportos - SAO ",
    " Belém - BEL "
]

timeGap = 0.5


class ExGOL(Extrair):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)

    def getUrl(self, origem, destino):
        self.driver.get("https://b2c.voegol.com.br/compra")
        time.sleep(timeGap)
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        # Set origin
        org = self.driver.find_element(By.ID, "input-saindo-de")
        time.sleep(timeGap)
        org.click()
        time.sleep(timeGap)
        org.send_keys("1")
        time.sleep(timeGap)
        elements = self.driver.find_elements(By.CLASS_NAME, "m-list-cta__item")
        for element in elements:
            if origem in element.text:
                element.click()
                break
        # Set destination
        dest = self.driver.find_element(By.ID, "input-indo-para")
        time.sleep(timeGap)
        dest.click()
        time.sleep(timeGap)
        dest.send_keys("1")
        time.sleep(timeGap)
        elements = self.driver.find_elements(By.CLASS_NAME, "m-list-cta__item")
        for element in elements:
            if destino in element.text:
                element.click()
                break

        # No site da gol é preciso usar ActionChains, porque em alguns estados como SP, o SAO não leva imediatamente à todos os aeroportos de SP, é preciso usar o scroll até chegar nele. Isso pode escalar até o ponto de ser necessário programar um comportamento para cada estado... Talvez se houvesse mais tempo eu conseguiria achar algum outro padrão para fazer a extração.

    def extrai(self):
        self.getUrl(estados[0], estados[1])


x = ExGOL()
x.extrai()
