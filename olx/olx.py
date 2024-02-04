def get_locations(driver):
    # clicking the set location box to show all regions
    driver.find_element("xpath", '//div[@class="b965ad08"]').click()

    time.sleep(0.5)

    locations_list = driver.find_elements("xpath", '//div[@class="_4b2c6986"]')
    current = driver.find_element("xpath", '//div[@class="d35d9456"]')
    all_locations = driver.find_element("xpath", '//div[@class="_7ebd8a86"]')
    locations = {}

    locations["current"] = current
    locations["all_locations"] = all_locations

    for location in locations_list:
        locations[location.text.strip()] = location

    return locations


def search_keyword(driver, keyword):
    input_box = driver.find_element("xpath", '//div[@class="_1075545d _1dc43551"]//input[@class="_162767a9"]')
    input_box.send_keys(keyword)
    search_btn = driver.find_element("xpath", '//div[@class="_1075545d _1dc43551"]//button').click()


import time
from collections import defaultdict

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs

options = Options()
# options.add_argument('--headless')
# options.add_argument(f"--proxy-server={'43.128.232.224:31993'}")
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.olx.com.pk/')

time.sleep(1)

# get all location names as keys and the selenium web element as values
locations_dict = get_locations(driver)

# set location from locations_dict
selected_location = locations_dict['Punjab, Pakistan']
selected_location.click()

search_input = "one plus"
search_keyword(driver, search_input)



print(locations_dict)

time.sleep(8)
