import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import logging
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging
logging.basicConfig(filename="scraping.log", level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for URL {url}: {e}")
        return None

def scrap_first_website(base_url, client):
    db = client.link1
    oscars = db.oscars

    soup = get_soup(base_url)
    if not soup:
        return

    base_website = soup.find_all("div", class_="col-md-12 text-center")
    websites = [i.text for i in base_website[0].find_all("a")]
    table_headers = [row.text for row in soup.find_all("table", class_="table")[0].find_next("tr").find_all("th")]

    def process_year(year):
        new_url = f"{base_url.split('#')[0]}#{year}"
        try:
            options = Options()
            options.headless = True
            options.add_argument("--window-size=1920,1080")
            options.add_argument("start-maximized")
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            
            driver = webdriver.Chrome(options=options)
            driver.get(new_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "film-title")))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find_all("table", class_="table")[0]
            for row in table.find_all("tr", class_="film"):
                col1 = row.find_all("td", class_="film-title")[0].text
                col2 = row.find_all(class_="film-nominations")[0].text
                col3 = row.find_all(class_="film-awards")[0].text
                best_picture = "best Picture" if row.find_all(class_="film-best-picture")[0].find("i", class_="glyphicon glyphicon-flag") else ""
                
                record = {
                    "film-title": col1,
                    "film-nominations": col2,
                    "film-awards": col3,
                    "film-best-picture": best_picture
                }
                oscars.insert_one(record)
            
            driver.quit()
        except Exception as e:
            logging.error(f"Error processing URL {new_url}: {e}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_year, year) for year in websites]
        for future in as_completed(futures):
            future.result()
            time.sleep(random.uniform(1, 3))  # Random delay

    print("Finished Scraping Website1")

def scrap_second_website(base_url, client):
    db = client.link2
    teams = db.teams

    soup = get_soup(base_url)
    if not soup:
        return

    pages = soup.find_all("ul", class_="pagination")[0]

    def process_page(link):
        new_url = base_url + link.a.get("href").split("/")[-1]
        soup = get_soup(new_url)
        if not soup:
            return

        table = soup.find_all("table", class_="table")[0]
        table_headers = [col.text.strip() for col in table.find_next("tr").find_all("th")]

        for row in table.find_all('tr'):
            row_content = {table_headers[i]: col.text.strip() for i, col in enumerate(row.find_all('td'))}
            teams.insert_one(row_content)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_page, link) for link in pages.find_all("li")[:-1]]
        for future in as_completed(futures):
            future.result()
            time.sleep(random.uniform(1, 3))  # Random delay

    print("Finished Scraping Website2")

def scrap_third_website(base_url, client):
    response = requests.get(base_url)
    if response.status_code != 200:
        logging.error(f"Failed to access {base_url}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    with open("Website3.txt", "w") as f:
        f.write(soup.prettify())

    print("Finished Scraping Website3")

if __name__ == "__main__":
    base_url1 = "https://www.scrapethissite.com/pages/ajax-javascript/#2015"
    base_url2 = "https://www.scrapethissite.com/pages/forms/"
    base_url3 = "https://www.scrapethissite.com/pages/advanced/"

    client = MongoClient("localhost", 27017)
    scrap_first_website(base_url1, client)
    scrap_second_website(base_url2, client)
    scrap_third_website(base_url3, client)
