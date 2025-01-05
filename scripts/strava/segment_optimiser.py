import getpass
import json
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

username = getpass.getuser()
service = Service()
# Set up options for headless Chrome
options = Options()
# options.add_argument("--blink-settings=imagesEnabled=false")
options.add_experimental_option("detach", True)
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(
    f"user-data-dir=/Users/{username}/Library/Application Support/Google/Chrome/Profile 1"
)
## options.add_argument("--disable-dev-shm-usage")
# options.page_load_strategy = (
#    "eager"  # Scraper doesn't wait for browser to load all the page
# )

# Initialize Chrome with the specified options
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)

activity_no = 13238398951
activity_dict_list = {"activities": []}
stat_dict_list = {"stats": []}

activity = "https://www.strava.com/activities/" + str(activity_no)
driver.get(activity)
time.sleep(np.abs(np.random.randn()))


segment_table = driver.find_element(
    By.CSS_SELECTOR, ".dense.hoverable.marginless.segments"
)


driver.find_elements(By.XPATH, '//*[@id="show-hidden-efforts"]')[0].click()
blocks = []
for j, segment in enumerate(segment_table.find_elements(By.TAG_NAME, "tr")):
    if j > 0:
        inside = []
        segment.click()
        time.sleep(4)
        clipper = driver.find_elements(By.CSS_SELECTOR, "[id^='view']")
        rects = clipper[0].find_elements(By.TAG_NAME, "rect")
        inside.append(segment.get_attribute("data-segment-effort-id"))
        inside.append(rects[0].get_attribute("x"))
        inside.append(
            float(rects[0].get_attribute("x")) + float(rects[0].get_attribute("width"))
        )
        for i, field in enumerate(segment.find_elements(By.TAG_NAME, "td")):
            if i == 3:
                inside.append(field.text.split("\n")[0])

        print(inside)
        blocks.append(inside)

print(len(blocks))

# segment_name = []
# for segment in segment_table.find_elements(By.TAG_NAME, "tr"):
#    for i, field in enumerate(segment.find_elements(By.TAG_NAME, "td")):
#        if i == 3:
#            segment_name.append(field.text.split("\n")[0])
# print(len(segment_name))
# print(segment_name)
# driver.quit()
