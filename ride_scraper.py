import random
import time

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
# options.add_argument("--blink-settings=imagesEnabled=false")
options.add_experimental_option("detach", True)
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(
    "user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile 1"
)
## options.add_argument("--disable-dev-shm-usage")
# options.page_load_strategy = (
#    "eager"  # Scraper doesn't wait for browser to load all the page
# )

pro_id = 1557033
date = 202428


def ride_scraper(pro_id, date):
    # Initialize Chrome with the specified options
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 5)
    homepage = (
        "https://www.strava.com/pros/"
        + str(pro_id)
        + "#interval?interval="
        + str(date)
        + "&interval_type=week&chart_type=miles&year_offset=0"
    )
    driver.get(homepage)
    time.sleep(30)
    activities = []
    for m in driver.find_elements(By.CSS_SELECTOR, "a[data-testid='activity_name']"):
        activities.append(m.get_attribute("href").split("/")[-1])
    driver.quit()
    conn.close()
    engine.dispose()
    return activities
