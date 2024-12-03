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


wait = WebDriverWait(driver, 5)
activity_no = 11888473406
activity = "https://www.strava.com/activities/" + str(activity_no)
driver.get(activity)
segment_table = driver.find_element(
    By.CSS_SELECTOR, ".dense.hoverable.marginless.segments"
)
segment_name = []
segment_distance = []
segment_vert = []
segment_grade = []
segment_time = []
segment_speed = []
watt = []
heart_rate = []
VAM = []
for segment in segment_table.find_elements(By.TAG_NAME, "tr"):
    for i, field in enumerate(segment.find_elements(By.TAG_NAME, "td")):
        if i == 3:
            segment_name.append(field.text.split("\n")[0])
            segment_distance.append(field.text.split("\n")[1].split(" ")[0])
            segment_vert.append(field.text.split("\n")[1].split(" ")[2])
            segment_grade.append(field.text.split("\n")[1].split(" ")[4].split("%")[0])
        elif i == 5:
            segment_time.append(field.text)
        elif i == 6:
            segment_speed.append(field.text.split(" ")[0])
        elif i == 7:
            watt.append(field.text.split(" ")[0])
        elif i == 8:
            VAM.append(field.text)
        elif i == 9:
            heart_rate.append(field.text.split("b")[0])

segment_dict = {
    "segment_name": segment_name,
    "segment_time": segment_time,
    "segment_speed": segment_speed,
    "watt": watt,
    "heart_rate": heart_rate,
    "segment_distance": segment_distance,
    "segment_vert": segment_vert,
    "segment_grade": segment_grade,
    "VAM": VAM,
}

df = pd.DataFrame.from_dict(segment_dict)
df.to_csv("segment.csv")

driver.quit()
conn.close()
engine.dispose()
