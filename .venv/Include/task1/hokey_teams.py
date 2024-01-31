import csv
import requests
from bs4 import BeautifulSoup as bs

keyword = ""
page_num = 1

print("enter keyword:")
keyword = input()
print("Searching...")

all_team_stats = []
team_stats = []
headers = ["Name", "Year", "Wins", "Losses", "OT Losses", "Win %", "Goals For (GF)", "Goals Against (GA)", "+ / -"]

url = requests.get(f'https://www.scrapethissite.com/pages/forms/?q={keyword}&per_page=100&page_num={str(page_num)}')

url_soap = bs(url.content, "lxml")
hokey_table = url_soap.find("table", class_ = "table")
total_pages = url_soap.find("ul", class_ =  "pagination")
total_pages = len(total_pages.find_all("li")) - 1

for page in range(page_num, total_pages):

    url = requests.get(f'https://www.scrapethissite.com/pages/forms/?q={keyword}&per_page=100&page_num={str(page_num)}')
    url_soap = bs(url.content, "lxml")
    hokey_table = url_soap.find("table", class_="table")

    for row in hokey_table.find_all("tr", class_ = "team"):
        for entry in row.find_all("td"):
            team_stats.append(entry.text.strip())

        all_team_stats.append(team_stats)
        team_stats = []

print(all_team_stats)




filename = "hokey_teams.csv"

with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(all_team_stats)
