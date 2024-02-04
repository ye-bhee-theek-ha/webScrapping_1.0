import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs

# options = Options()
# # options.add_argument('--headless')
#
# service = Service(ChromeDriverManager().install())
#
# driver = webdriver.Chrome(service=service, options=options)
# driver.get('https://whatismyipaddress.com/')
#
# WebDriverWait(driver, 10).until(
#     EC.visibility_of_element_located((By.CSS_SELECTOR, "span[id='ipv4']"))
# )
#
# source = bs(driver.page_source, "lxml")
# ip = source.find("span", id="ipv4")
#
# print(ip.text.strip())

# driver.quit()