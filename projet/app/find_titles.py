from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

import time
import os 
c_dir = os.path.dirname(os.path.realpath(__file__))


def select_drop_list(driver, component_id, index):
    xpath = "//select[@id='" + component_id + "']"
    dd = Select(driver.find_element_by_xpath(xpath))
    dd.select_by_index(index)
    time.sleep(2)

def get_companies_from_web_page(html):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id="investor").find("tbody")
    companies = []
    for row in table.findChildren("tr" , recursive=False):
        childs = row.findAll("td")
        company_name = childs[1].find("a").text
        company_ticker = childs[2].find("a").text
        companies.append((company_name, company_ticker))
    return companies


def get_pages_number(html):
    soup = BeautifulSoup(html, "lxml")
    return soup.find("table", id="investor").find("span").findChildren("a" , recursive=False)[-1]


# Returns 100 companies from a particular sector. Input correpsonding index
# 1 - cpc
# 2 - Clean Technologies
# 3 - Closed-End Funds
# 4 - Comm & Media
# 5 - Diversified industries
# 6 - ETP
# 7 - Financial services
# 8 - Forest Products and paper
# 9 - Life Science
# 10 - Mining
# 11 - Oil and gas
# 12 - Real Estate
# 13 - Technology
# 14 - Utilities & Pipeline
def get_companies(sector_index, market_cap_index=5):
    if sector_index not in range(1,15):
        exit("sector_index must be between 1 and 15")
    if market_cap_index not in range(1,6):
        exit("sector_index must be between 1 and 5")
    
    # TODO: use firefox or google
    driver = webdriver.Chrome(os.path.join(c_dir, "chromedriver"))
    driver.get('https://api.tmxmoney.com/fr/migreport/search')

    time.sleep(20)

    select_drop_list(driver, 'id_exchanges', 1)
    select_drop_list(driver, 'id_sectors', sector_index)
    select_drop_list(driver, 'id_marketcap', market_cap_index)


    # Next page
    driver.execute_script("window.scrollTo(0, 0.3*document.body.scrollHeight);")
    time.sleep(2)
    research_button = driver.find_element_by_xpath("//input[@value='Recherche']")
    research_button.click()
    time.sleep(25)

    #More results
    dd = Select(driver.find_element_by_xpath("//select[@name='investor_length']"))
    dd.select_by_value("100")
    time.sleep(10)
    
    # Parse document
    html = driver.page_source
    companies = get_companies_from_web_page(html)
    driver.close()
    return companies


if __name__ == "__main__":
    cop = get_companies(1)
    print(cop)