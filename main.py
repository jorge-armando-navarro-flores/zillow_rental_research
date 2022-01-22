import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import os
from bs4 import BeautifulSoup

CHROME_DRIVER_PATH = os.environ.get("DRIVER_PATH")
SIMILAR_ACCOUNT = "chefsteps"
USERNAME = os.environ.get("USERNMAME")
PASSWORD = os.environ.get("PASSWORD")
HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }


class ZillowRentalResearch:

    def __init__(self):
        self.headers = HEADERS
        self.properties_url = "https://www.zillow.com/homes/for_rent/1-_beds/1.0-_baths/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122.23248518896484%2C%22south%22%3A37.67413744795903%2C%22north%22%3A37.87630724732759%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%7D"
        self.driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))
        self.data = {}

    def scrape_data(self):
        domain = "https://www.zillow.com"
        response = requests.get(self.properties_url, headers=self.headers)
        website_html = response.text
        soup = BeautifulSoup(website_html, "html.parser")

        a_tags = soup.select(".list-card-top a")
        links = []
        for tag in a_tags:
            link = tag.get("href")
            if domain in link:
                links.append(link)
            else:
                links.append(domain + link)

        price_tags = soup.select(".list-card-price")
        prices = []
        for tag in price_tags:
            price_text = tag.getText()
            if "/" in price_text:
                price = price_text.split("/")[0]
            else:
                price = price_text.split("+")[0]
            prices.append(price)

        address_tags = soup.select(".list-card-info a address")
        addresses = [tag.getText().split(" | ")[-1] for tag in address_tags]

        print(links)
        print(prices)
        print(addresses)

        self.data["addresses"] = addresses
        self.data["prices"] = prices
        self.data["links"] = links


    def fill_form(self):

        self.driver.get("https://forms.gle/Vrb9ThYqn7LCGQuq7")
        for i in range(len(self.data["addresses"])):
            sleep(2)
            address = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            address.send_keys(self.data["addresses"][i])
            price = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price.send_keys(self.data["prices"][i])
            link = self.driver.find_element(By.XPATH,
                                             '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link.send_keys(self.data["links"][i])

            send = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
            send.click()
            sleep(2)
            another_answer = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            another_answer.click()

bot = ZillowRentalResearch()
bot.scrape_data()
bot.fill_form()




