import random
import time

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine, inspect, text

engine = create_engine("mysql+mysqldb://root:Abrakadabra69!@127.0.0.1:3306/grand_tours")
conn = engine.connect()

name_query = "SELECT DISTINCT(`name`) FROM tdf_database WHERE `year` = 2024 "

service = Service()
# Set up options for headless Chrome
options = Options()
# options.headless = True  # Enable headless mode for invisible operation
# options.add_argument("--window-size=1920,1200")  # Define the window size of the browser
# options.add_experimental_option("detach", True)

# options.add_argument("--no-sandbox")
# options.add_argument("--headless")
# options.add_argument("--no-proxy-server")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(
    "user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile 1"
)
## options.add_argument("--disable-dev-shm-usage")
options.page_load_strategy = (
    "eager"  # Scraper doesn't wait for browser to load all the page
)

# Initialize Chrome with the specified options
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 3)
activity = "https://www.strava.com/activities/11888473406"
driver.get(activity)
summary_container = driver.find_element(
    By.CSS_SELECTOR, ".row.no-margins.activity-summary-container"
)
summary_pre = summary_container.text.split("\n")[0].split(",")
date = summary_pre[1] + " " + summary_pre[2].split(" ")[1]
distance = summary_container.text.split("\n")[
    summary_container.text.split("\n").index("Distance") - 1
].split(" ")[0]
for i in driver.find_elements(By.XPATH, "//*[@id='heading']/header/h2/span/a"):
    name = i.get_attribute("href").split("/")[-1]

athlete_id = driver.find_element(
    By.XPATH, "//*[@id='heading']/header/h2/span/a"
).get_attribute("href")


print(date, distance, name, athlete_id)
driver.quit()
conn.close()
engine.dispose()
