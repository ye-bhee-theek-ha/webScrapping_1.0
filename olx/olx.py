def scroll_to_bottom(driver, prev_height):
    driver.execute_script(f"window.scrollTo({prev_height}, {prev_height + 10});")


def get_locations(driver):
    # clicking the set location box to show all regions
    driver.find_element("xpath", '//div[@class="b965ad08"]').click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(("xpath", "//div[@class='_7ebd8a86']"))
    )

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
    input_box_xpath = ('//div[@class="_1075545d _1dc43551"]'
                       '//input[@class="_162767a9"]')
    input_box = driver.find_element("xpath", input_box_xpath)
    input_box.send_keys(keyword)
    driver.find_element("xpath", '//div[@class="_1075545d _1dc43551"]//button').click()


def get_sort_options(driver):
    sort_by = {}

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(("xpath", "//div[@class='_1075545d bfd72c21 _96d4439a']"))
    )

    driver.find_element(By.CSS_SELECTOR, "button.a8869a31").click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(("xpath", "//ul[@class='f44ebfb0']"))
    )

    for option in driver.find_elements("xpath", "//ul[@class='f44ebfb0'][@role='listbox']//li"):
        sort_by[option.text.strip()] = option

    return sort_by


def load_all(driver, pages):

    for i in range(0, pages):
        driver.find_element("xpath", "//a[@class='_95dae89d']").click()
        time.sleep(6)
        scroll_to_bottom(driver, 0)


import time
import csv

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
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

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(("xpath", "//div[@class='f6ca0ff5']"))
)
# HOME PAGE

# get all location names as keys and the selenium web element as values
locations_dict = get_locations(driver)

# set location from locations_dict
selected_location = locations_dict['Punjab, Pakistan']
selected_location.click()

search_input = "one plus"
search_keyword(driver, search_input)

required_ads = 50
required_pages = int(required_ads / 20)
print(required_pages)

# KEYWORD PAGE
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(("xpath", "//div[@class='_1075545d _5f872d11']"))
)
total_ads_str = driver.find_element("xpath", "//div[@class='_76047990']").text.strip()
total_ads = "".join(c for c in total_ads_str if c.isnumeric())
print(total_ads)
print(total_ads_str)


# sort by
sort_by_options_dict = get_sort_options(driver)

selected_option = sort_by_options_dict['Most relevant']
selected_option.click()

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(("xpath", "//div[@class='a52608cc']"))
)

load_all(driver, required_pages)

all_ads_list = []

# scraping data
all_ads_xpath = ("//ul[@class='ba608fb8 de8df3a3']"
                 "//li[@aria-label='Listing']"
                 "//div[@class='a52608cc']")

all_ads = driver.find_elements("xpath", all_ads_xpath)

for ad in all_ads:
    source = bs(ad.get_attribute("innerHTML"), "lxml")

    content_list = [source.select_one(".fc10b949._5fdf4379").text.strip(),  # title[0]
                    source.select_one("a")['href'],  # link[1]
                    source.select_one("._1075545d._52497c97._96d4439a").text.strip(),  # price[2]
                    source.select_one("div.e48cb10f").contents[0].text.strip(),  # location[3]
                    source.select_one("div.e48cb10f").contents[1].text.strip()]   # date_posted[4]

    all_ads_list.append(content_list)

    if len(all_ads_list) == required_ads:
        break


print(total_ads)
for ad in all_ads_list:
    print(ad)

headers = ['title', 'link', 'price', 'location', 'time']
file = "OLX_ads.csv"

with open(file, 'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    writer.writerow(headers)
    writer.writerows(all_ads_list)

