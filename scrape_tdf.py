import csv
import os
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Set up options for headless Chrome
options = Options()
options.headless = True  # Enable headless mode for invisible operation
options.add_argument("--window-size=1920,1200")  # Define the window size of the browser


# Initialize Chrome with the specified options
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

driver.get("https://www.letour.fr/en/history")
driver.implicitly_wait(10)
# cookie accept
wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

year_dd = driver.find_element(By.CSS_SELECTOR, ".custom-select.custom-select--year")
year_options = year_dd.find_elements(By.TAG_NAME, "option")


stages_dd = driver.find_element(By.ID, "stageSelect")
stages = stages_dd.find_elements(By.TAG_NAME, "option")
driver.implicitly_wait(10)
# print(stages[3].get_attribute("text"))


# stages_dd = driver.find_elements(By.CSS_SELECTOR, ".select-items")
# stages = stages_dd[-2].find_elements(By.TAG_NAME, "div")
#

the_soup = BeautifulSoup(driver.page_source, "html.parser")

rankings = the_soup.find_all(
    "table", attrs={"class": "rankingTable rtable js-extend-target"}
)
riders = rankings[0].findChildren("tr")[1:]

names = the_soup.find_all("td", attrs={"class": "runner"})
print(riders)

# year_lst = []
# for year in year_options:
#    year_lst.append(year.get_attribute("text"))
#    # year.click()
#    # time.sleep(2)
#    # year_val = year.get_attribute("text")
#    # year_lst.append(year_val)
# print(year_lst)

# stages_lst = []
# for stage in stages:
#    wait.until(EC.element_to_be_clickable(stage)).click()
#    driver.implicitly_wait(10)
#    stage_val = stage.get_attribute("text")
#    stages_lst.append(stage_val)
# print(stages_lst)
#
##
# name_lst = []
# for name in names:
#    name_lst.append(name.text.strip())  # rider names
#
# timing_lst = []
# for rider in riders:
#    timing_lst.append(
#        rider.findChildren("td", attrs={"class": "is-alignCenter"})[1].text
#    )  # riders attributes, index 1 is total time
#
# df = pd.DataFrame({"name": name_lst, "timing": timing_lst})
# print(df)
