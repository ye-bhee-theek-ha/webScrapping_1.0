import time
from collections import defaultdict

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

year = ["2015", "2014", "2013", "2012", "2011", "2010"]
movie_data = []
movies_in_year = []
database = defaultdict(list)

service = Service(executable_path= "./chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.scrapethissite.com/pages/ajax-javascript/#2015")

for year in year:

    movies_in_year = []

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "film"))
    )

    year_btn = driver.find_element(By.ID, year)
    year_btn.click()

    time.sleep(4)

    table = driver.find_element(By.ID, "table-body")
    source_table = bs(table.get_attribute("innerHTML"), "lxml")
    rows = source_table.find_all("tr", class_ = "film")
    for row in rows:
        movie_data = []
        for entry in row.find_all("td"):
            movie_data.append(entry.text.strip())

        movies_in_year.append(movie_data)

    database[year].append(movies_in_year)

keys = database.keys()

for key in keys:
    print(f"{key} :")
    print(database[key])
    print("\n\n-------------------------\n\n")







