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
# options.headless = True  # Enable headless mode for invisible operation
options.add_argument("--window-size=1920,1200")  # Define the window size of the browser
options.add_experimental_option("detach", True)

# Initialize Chrome with the specified options
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)


driver.get("https://www.letour.fr/en/history")
driver.implicitly_wait(10)

wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))

driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "/html/body/div[2]/main/div[1]/section[1]/div/div[1]/div/div/div/div[1]/div",
        )
    )
)
driver.find_element(
    By.XPATH,
    "/html/body/div[2]/main/div[1]/section[1]/div/div[1]/div/div/div/div[1]/div",
).click()

wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "/html/body/div[2]/main/div[1]/section[1]/div/div[2]/div[111]/div[3]/div[2]/div[1]/div[1]/div[1]",
        )
    )
)
driver.find_element(
    By.XPATH,
    "/html/body/div[2]/main/div[1]/section[1]/div/div[2]/div[111]/div[3]/div[2]/div[1]/div[1]/div[1]",
).click()

# wait.until(
#    EC.presence_of_element_located(
#        (By.CSS_SELECTOR, ".select-selected.select-arrow-active")
#    )
# )

# stages_dd = driver.find_element(
#    "xpath", "//*[@id=2023]/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]"
# )

# stages_dd = wait.until(
#    EC.element_to_be_clickable(
#        driver.find_element(By.CSS_SELECTOR, ".select-selected.select-arrow-active")
#    )
# ).click()
# print(stages_dd)
# stages = stages_dd.find_elements(By.TAG_NAME, "div")
# print(len(stages))
# driver.implicitly_wait(10)
# print(stages[3].get_attribute("text"))


# stages_lst = []
# for stage in stages:
#    wait.until(EC.element_to_be_clickable(stage)).click()
#    driver.implicitly_wait(10)
#    stage_val = stage.get_attribute("text")
#    stages_lst.append(stage_val)
# print(stages_lst)

#
