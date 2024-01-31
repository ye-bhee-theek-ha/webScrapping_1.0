import requests
from bs4 import BeautifulSoup as bs
import csv


task_0 = requests.get("https://www.scrapethissite.com/pages/simple/")

task_0_soup = bs(task_0.content, 'lxml')
main_container = task_0_soup.find("div", id= "page" )
all_countries = main_container.find_all("div", class_ = "country")

countries_list = {}

for country in all_countries:
    name = country.find("h3").text.strip()
    capital = country.find("span", class_ = "country-capital").text.strip()

    countries_list[name] = capital

print(countries_list)

data_file = open("data.txt", "w", encoding="utf-8")
i = 1

for country, capital in countries_list.items():
    data_file.write(str(i) + ". " + (country) + " => " + (capital) + "\n")
    i = i + 1
