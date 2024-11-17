import csv
import os
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

# Set up options for headless Chrome
options = Options()
options.headless = True  # Enable headless mode for invisible operation
options.add_argument("--window-size=1920,1200")  # Define the window size of the browser


# Initialize Chrome with the specified options
driver = webdriver.Chrome(options=options)

driver.get("https://www.letour.fr/en/history")
driver.implicitly_wait(10)

year_dd = driver.find_element(By.CSS_SELECTOR, ".custom-select.custom-select--year")
year_options = year_dd.find_elements(By.TAG_NAME, "option")

stages_dd = driver.find_element(By.CSS_SELECTOR, ".custom-select.custom-select--expand")
stages = stages_dd.find_elements(By.TAG_NAME, "option")
rank_table = driver.find_element(
    By.CSS_SELECTOR, ".rankingTable.rtable.js-extend-target"
)
# rankings = rank_table.find_elements(By.TAG_NAME, "tr")
# print(rankings)

# gender_dd = driver.find_element(By.ID, "athlete_gender")
# gender_options = gender_dd.find_elements(By.TAG_NAME, "option")
#
#
# usa_lst = []
#
year_lst = []
for year in year_options:
    year_lst.append(year.get_attribute("text"))
    # year.click()
    # time.sleep(2)
    # year_val = year.get_attribute("text")
    # year_lst.append(year_val)
print(year_lst)

stages_lst = []
for stage in stages:
    stages_lst.append(stage.get_attribute("text"))
    # year.click()
    # time.sleep(2)
    # year_val = year.get_attribute("text")
    # year_lst.append(year_val)
print(stages_lst)

the_soup = BeautifulSoup(driver.page_source, "html.parser")

rankings = the_soup.find(
    "table", attrs={"class": "rankingTable rtable js-extend-target"}
)
riders = rankings.findChildren("tr")[1:]

print(riders[2].findChildren("td", attrs={"class": "is-alignCenter"}))

names = the_soup.find_all("td", attrs={"class": "runner"})
#
name_lst = []
for name in names:
    name_lst.append(name.text.strip())  # rider names

timing_lst = []
for rider in riders:
    timing_lst.append(
        rider.findChildren("td", attrs={"class": "is-alignCenter"})[1].text
    )  # riders attributes, index 1 is total time

df = pd.DataFrame({"name": name_lst, "timing": timing_lst})
print(df)
