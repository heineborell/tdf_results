import csv
import os
import re
import time

import numpy as np
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
options.add_experimental_option("detach", True)


# Initialize Chrome with the specified options
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

driver.get("https://www.letour.fr/en/history")
driver.implicitly_wait(10)
# cookie accept
wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

# choose individual drop down
driver.find_element(
    By.XPATH,
    "//*[@id='2024']/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]",
).click()
# individual select
driver.find_element(
    By.XPATH,
    "//*[@id='2024']/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]",
).click()
time.sleep(2)
# next table rankings button this has to be in the stage loop
wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[@id="2024"]/div[3]/div[2]/div[1]/div[3]/a')
    )
)
driver.find_element(By.XPATH, '//*[@id="2024"]/div[3]/div[2]/div[1]/div[3]/a').click()
time.sleep(2)

table = driver.find_element(
    By.XPATH, '//*[@id="2024"]/div[3]/div[2]/div[1]/div[2]/table'
)
cyclists = table.find_elements(By.TAG_NAME, "tr")
ranking = np.zeros(3)
for cyclist in cyclists:
    attrs = cyclist.find_elements(By.TAG_NAME, "td")
    attr_list = []
    for i, attr in enumerate(attrs):
        if i == 1 or i == 2 or i == 3:
            attr_list.append(attr.text)
    if len(attr_list) == 3:
        ranking = np.vstack([ranking, attr_list])

print(ranking)
print(ranking[1, 2])
# print(attr_list)

# ranking = np.stack((ranking, attr_list))
# year_dd = driver.find_element(By.CSS_SELECTOR, ".custom-select.custom-select--year")
# year_options = year_dd.find_elements(By.TAG_NAME, "option")
#
#
# stages_dd = driver.find_element(By.ID, "stageSelect")
# stages = stages_dd.find_elements(By.TAG_NAME, "option")
# driver.implicitly_wait(10)
#
# wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
#
# driver.find_element(By.ID, "onetrust-accept-btn-handler").click()  # cookie accept
#
# year_dd = driver.find_element(
#    By.XPATH,
#    "/html/body/div[2]/main/div[1]/section[1]/div/div[1]/div/div/div/div[1]/div",
# )
# year_options = driver.find_elements(
#    By.XPATH,
#    "//html/body/div[2]/main/div[1]/section[1]/div/div[1]/div/div/div/div[1]/div/div[2]/div",
# )
#
# year_len = len(year_options)
#
# year_extr = driver.find_element(By.CSS_SELECTOR, ".custom-select.custom-select--year")
# year_lst = [
#    year.get_attribute("text")
#    for year in year_extr.find_elements(By.TAG_NAME, "option")
# ]
# print(year_lst)
#

# the_soup = BeautifulSoup(driver.page_source, "html.parser")
#
# rankings = the_soup.find_all(
#    "table", attrs={"class": "rankingTable rtable js-extend-target"}
# )
# riders = rankings[0].findChildren("tr")[1:]
#
# names = the_soup.find_all("td", attrs={"class": "runner"})
# print(riders)
