from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from load_json_players import read_json

class MyDriver():
    ''' Create list of urls for futher BeatifulSoup scraping '''
    urls_list = []

    def setup_method(self):
        print("setup method")
        self.driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe')
        self.input_search()
        
    def accept_cookies(self):
        self.driver.get('https://basketball-reference.com')
        try:
            #Accept cookies policy
            agree_policy_button = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]/span')))
        finally:
            #Insert text into search_input
            agree_policy_button.click()

    def input_search(self):
        #List of nba player from json
        players = read_json()
        self.accept_cookies()
        for player in players:
            try:
                #Find main search input
                search_input = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div[3]/form/div/div/input[2]'))
                )
            finally:
                #Insert text into search_input
                search_input.send_keys(player)
                try:
                    #Find result from input
                    result_element = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div[3]/form/div/div/div/div[1]/div[2]/div/div/span[2]'))
                )
                finally:
                    #Click result
                    result_element.click()
                    # Append urls to list
                    self.urls_list.append(self.driver.current_url)
        self.driver.quit()

driver = MyDriver()
driver.setup_method()


