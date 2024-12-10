"""This script scrapes the strava pro ids given their names"""

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

name_query = "SELECT DISTINCT(`name`) FROM tdf_database WHERE `year` > 2010 "

service = Service()
# Set up options for headless Chrome
options = Options()
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(
    "user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile 1"
)
options.page_load_strategy = (
    "eager"  # Scraper doesn't wait for browser to load all the page
)

# Initialize Chrome with the specified options
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)
df_names = pd.read_sql_query(name_query, conn)


# surname-name reverse
def split_from_first_lowercase(s):
    for i, char in enumerate(s):
        if char.islower():
            return s[: i - 1], s[i - 1 :]


name_list = [split_from_first_lowercase(name) for name in df_names.name]
strava_df = pd.DataFrame(columns=["name", "strava_id"])
for name in name_list:
    time.sleep(np.abs(np.random.randn()))
    strava_dict = {}
    driver.get("https://www.strava.com/athletes/search")
    athlete_name = driver.find_element(By.CLASS_NAME, "inline-inputs")
    search_field = athlete_name.find_elements(By.TAG_NAME, "input")
    search_field[0].send_keys(name[1] + " " + name[0])  # insert field
    search_field[1].click()  # submit search
    time.sleep(random.randint(1, 2))
    try:
        athelete = driver.find_element(
            By.XPATH,
            "//*[contains(@class, 'app-icon') and contains(@class, 'icon-badge-pro')]/ancestor::*[contains(@class, 'spans6')]",
        )
        athelete_details = athelete.find_element(By.CLASS_NAME, "athlete-details")
        print(athelete_details.text.split("\n")[0])
        print(
            athelete_details.find_element(By.CLASS_NAME, "follow-action").get_attribute(
                "data-athlete-id"
            )
        )
        strava_dict.update(
            {
                "name": [name[0] + name[1]],
                "strava_id": [
                    athelete_details.find_element(
                        By.CLASS_NAME, "follow-action"
                    ).get_attribute("data-athlete-id")
                ],
            }
        )
    except NoSuchElementException:
        strava_dict.update({"name": [name[0] + name[1]], "strava_id": [np.nan]})
        print(f"No strava account for {name}")

    strava_df = pd.concat([strava_df, pd.DataFrame.from_dict(strava_dict)])
    strava_df.to_csv(
        "strava_ids_fin.csv"
    )  # Note that the end result will have null fields for the strava_id column


driver.quit()
conn.close()
engine.dispose()
