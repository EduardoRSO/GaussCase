from selenium.webdriver.remote.webelement import WebElement
from AnaliseDados import Extrair
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.webdriver import *
import random
import cloudscraper
# import undetected_chromedriver as uc NAO FUNCIONOU...
# https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver
# https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec
# https://stackoverflow.com/questions/53039551/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detec/53040904#53040904
# https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver
# https://stackoverflow.com/questions/56528631/is-there-a-version-of-selenium-webdriver-that-is-not-detectable/56529616#56529616
# https://stackoverflow.com/questions/68895582/how-to-avoid-a-bot-detection-and-scrape-a-website-using-python


class ExAZUL(Extrair):

    def __init__(self):
        # Create Chromeoptions instance
        options = webdriver.ChromeOptions()

        # IP Rotation / Proxy

        # proxy = "11.456.448.110:8080"

        # options.add_argument("--proxy-server=%s" % proxy)

        # Disabling the automation indicator webdriver flags

        # Adding argument to disable the AutomationControlled flag
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Exclude the collection of enable-automation switches
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])

        # Turn-off userAutomationExtension
        options.add_experimental_option("useAutomationExtension", False)

        # Keep windows alive
        options.add_experimental_option("detach", True)

        # Headless No momento só atrapalha...
        # options.add_argument("--headless=new")

        # Setting the driver path and requesting a page
        self.driver = webdriver.Chrome(options=options)

        # Changing the property of the navigator value for webdriver to undefined
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Rotating HTTP Header Information and User-Agent

        useragentarray = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",]

        self.driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            "userAgent": useragentarray[random.randint(0, 1)]})
        # self.driver = uc.Chrome() Não funcionou...

    def scrape(self, origem, destino, dtIda, dtVolta):
        """Retira os dados no contexto da AZUL"""
        # self.url = "https://www.voeazul.com.br/br/pt/home/selecao-voo?c[0].ds={ORIGEM}&c[0].std={DTIDA}&c[0].as={DESTINO}&c[1].ds={DESTINO}&c[1].std={DTVOLTA}&c[1].as={ORIGEM}&p[0].t=ADT&p[0].c=1&p[0].cp=false&f.dl=3&f.dr=3&cc=BRL".format(            ORIGEM = origem, DESTINO = destino, DTIDA = dtIda, DTVOLTA = dtVolta)
       # self.url = "https://www.voeazul.com.br/br/pt/home/selecao-voo?c[0].ds=SAO&c[0].std=08/26/2023&c[0].as=MAO&c[1].ds=MAO&c[1].std=08/27/2023&c[1].as=SAO&p[0].t=ADT&p[0].c=1&p[0].cp=false&f.dl=3&f.dr=3&cc=BRL"
        self.url = "https://www.latamairlines.com/br/pt/oferta-voos?dataFlight=%7B%22tripTypeSelected%22%3A%7B%22label%22%3A%22Solo%20ida%22%2C%22value%22%3A%22OW%22%7D%2C%22cabinSelected%22%3A%7B%22label%22%3A%22Economy%22%2C%22value%22%3A%22Economy%22%7D%2C%22passengerSelected%22%3A%7B%22adultQuantity%22%3A1%2C%22childrenQuantity%22%3A0%2C%22infantQuantity%22%3A0%7D%2C%22originSelected%22%3A%7B%22id%22%3A%22SAO_BR_CITY%22%2C%22name%22%3A%22null%22%2C%22city%22%3A%22S%C3%A3o%20Paulo%22%2C%22cityIsoCode%22%3A%22SAO%22%2C%22country%22%3A%22Brasil%22%2C%22iata%22%3A%22SAO%22%2C%22latitude%22%3A-23.55052%2C%22longitude%22%3A-46.633309%2C%22timezone%22%3A-3%2C%22tz%22%3A%22America%2FSao_Paulo%22%2C%22type%22%3A%22CITY%22%2C%22countryAlpha2%22%3A%22BR%22%2C%22allAirportsText%22%3A%22xp_sales_web_searchbox_od_allAirports%22%2C%22airportIataCode%22%3A%22SAO%22%7D%2C%22destinationSelected%22%3A%7B%22id%22%3A%22MAO_BR_AIRPORT%22%2C%22name%22%3A%22Eduardo%20Gomes%22%2C%22city%22%3A%22Manaus%22%2C%22cityIsoCode%22%3A%22MAO%22%2C%22country%22%3A%22Brasil%22%2C%22iata%22%3A%22MAO%22%2C%22latitude%22%3A-3.0386099815368652%2C%22longitude%22%3A-60.04970169067383%2C%22timezone%22%3A-4%2C%22tz%22%3A%22America%2FBoa_Vista%22%2C%22type%22%3A%22AIRPORT%22%2C%22countryAlpha2%22%3A%22BR%22%2C%22allAirportsText%22%3Anull%2C%22airportIataCode%22%3A%22MAO%22%7D%2C%22dateGoSelected%22%3A%222023-08-26T15%3A00%3A00.000Z%22%2C%22dateReturnSelected%22%3Anull%2C%22redemption%22%3Afalse%7D"
      #  print(self.url)

        #
        # Cloudscraper try
        #

        # scraper = cloudscraper.create_scraper()
        # print(scraper.get(self.url).text)
        self.driver.get(self.url)
        # self.driver.maximize_window()
        # time.sleep(10)
        # self.driver.implicitly_wait(30)
       # self.driver.execute_script("window.stop();")
       # WebDriverWait(self.driver, 10).until(
        #    EC.presence_of_element_located((By.ID, "load-more-button")))
       # element = self.driver.find_element(By.ID, "load-more-button").click()
        # element = self.driver.find_element(
        #    By.XPATH, "/html/body/div[2]/div[3]/div/div/div/div/div/div[2]/div[1]/button").click()
        element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[3]/div/div/div/div/div/div[2]/div[1]/button"))
        )
        element.click
        # content = self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        time.sleep(5)
        soup = bs(self.driver.page_source, "html.parser")
        # div = soup.find_all("div", class_="card flight-card")
        print(soup.prettify())
     #   self.driver.close()


x = ExAZUL()
x.scrape("SAO", "MAO", "08/26/2023", "08/27/2023")
