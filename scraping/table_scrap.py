from bs4 import BeautifulSoup
import requests
import pandas as pd
from bask_ref_scrap import MyDriver
from load_json_players import read_json

class Table():

    columns_dict = {}
    columns_with_stats_dict = {}
     
    def get_columns(self):
        #Just one url to get table columns
        url = 'https://www.basketball-reference.com/players/j/jamesle01.html'
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        #Find table per_game and columns names
        table = soup.find('table', {'id':'per_game'}).find_all('th', {'scope':'col'})
        '''
        child.text: this will be column name
        formated_data_trip: explanation of column name, could be used in next data analyst steps

        '''
        for child in table:
            if child.text != 'Season':
                # Get data-tip attribute and remove unecessary strings
                formated_data_trip = child.attrs['data-tip'].replace('<br>','').replace('<strong>','').replace('</strong>','')
                self.columns_dict[child.text] = formated_data_trip

    def create_column_dict(self):
        '''Create dictionary with empty lists as values'''
        for key in self.columns_dict.keys():
            self.columns_with_stats_dict[key] = []
        self.columns_with_stats_dict['Players'] = []

    def create_dataframe(self):
        driver = MyDriver()
        urls = driver.setup_method()
        for url in urls:
            print(url)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            row_2022 = soup.find('table', {'id':'per_game'}).find('tr', {'id':'per_game.2022'})
            if row_2022 != None:
                # Find player name
                player_name = soup.find('div', {'id':'info'}).find('h1').text.replace('\n','')
                self.columns_with_stats_dict['Players'].append(player_name)
                row_2022 = soup.find('table', {'id':'per_game'}).find('tr', {'id':'per_game.2022'}).find_all('td')
                for (row,key) in zip(row_2022,self.columns_dict.keys()):
                    self.columns_with_stats_dict[key].append(row.text)
        df = pd.DataFrame(self.columns_with_stats_dict).set_index('Players')
        df.to_csv('.\\data\\csv\\nba_players_data.csv')
        return df

table = Table()
table.get_columns()
table.create_column_dict()
table.create_dataframe()