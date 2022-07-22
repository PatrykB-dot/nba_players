from bs4 import BeautifulSoup
import requests
import pandas as pd
from bask_ref_scrap import MyDriver
from load_json_players import read_json

url = 'https://www.basketball-reference.com/players/j/jamesle01.html'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
columns_dict = {}
table = soup.find('table', {'id':'per_game'}).find_all('th', {'scope':'col'})
for child in table:
    if child.text != 'Season':
        formated_data_trip = child.attrs['data-tip'].replace('<br>','').replace('<strong>','').replace('</strong>','')
        columns_dict[child.text] = formated_data_trip

columns_with_stats_dict = {}
for key in columns_dict.keys():
    columns_with_stats_dict[key] = []

columns_with_stats_dict['Players'] = read_json()

driver = MyDriver()
urls = driver.setup_method()
for url in urls:
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    row_2022 = soup.find('table', {'id':'per_game'}).find('tr', {'id':'per_game.2022'}).find_all('td')
    for (row,key) in zip(row_2022,columns_dict.keys()):
        columns_with_stats_dict[key].append(row.text)


df = pd.DataFrame(columns_with_stats_dict).set_index('Players')
print(df)
