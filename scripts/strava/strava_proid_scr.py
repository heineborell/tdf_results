"""This script scrapes the strava pro ids given their names"""

import getpass
import random
import sqlite3
import time

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

username = getpass.getuser()

name_query = " SELECT name FROM tdf_results WHERE year > 2010 UNION SELECT name FROM giro_results WHERE year > 2010 UNION SELECT name FROM vuelta_results WHERE year > 2010"

conn = sqlite3.connect(
    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db"
)

df_names = pd.read_sql_query(name_query, conn)
df_collected =pd.read_csv(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/strava_ids.csv", 
                      usecols=["name", "strava_id"]) # these are the ones I already collected from tdf and giro
merged = df_names.merge(df_collected,'left',['name'],indicator=True)
df_names = (merged.loc[merged['_merge'] == 'left_only'].drop(columns = ['_merge','strava_id']))
service = Service()
# Set up options for headless Chrome
options = Options()
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(
    f"user-data-dir=/Users/{username}/Library/Application Support/Google/Chrome/Profile 1"
)
options.page_load_strategy = (
    "eager"  # Scraper doesn't wait for browser to load all the page
)

# Initialize Chrome with the specified options
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)


# surname-name reverse
def split_from_first_lowercase(s):
    for i, char in enumerate(s):
        if char.islower():
            return s[: i - 1], s[i - 1 :]


name_list = [split_from_first_lowercase(name) for name in df_names.name]
print(len(name_list))
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
        "~/iCloud/Research/Data_Science/Projects/data/strava/strava_ids_therest.csv"
    )  # Note that the end result will have null fields for the strava_id column


driver.quit()
conn.close()
