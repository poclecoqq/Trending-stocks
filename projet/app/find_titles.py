from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

import time
import os 




c_dir = os.path.dirname(os.path.realpath(__file__))

# TODO: use firefox or google
driver = webdriver.Chrome(os.path.join(c_dir, "chromedriver"))
driver.get('https://api.tmxmoney.com/fr/migreport/search')

# Premier click
time.sleep(2)
research_button = driver.find_element_by_xpath("//input[@value='Recherche']")
driver.execute_script("window.scrollTo(0, 0.3*document.body.scrollHeight);")
time.sleep(2)
research_button.click()

#Deuxième click
time.sleep(15)
time.sleep(15)
dd = Select(driver.find_element_by_xpath("//select[@name='investor_length']"))
dd.select_by_value("100") 
print("yaz")
time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, "lxml")
table = soup.find("table", id="investor").find("tbody")
companies = []
for row in table.findChildren("tr" , recursive=False):
    childs = row.findAll("td")
    company_name = childs[1].find("a").text
    company_ticker = childs[2].find("a").text
    companies.append((company_name, company_ticker))
print(companies)
#Fermeture du fichier
driver.close()