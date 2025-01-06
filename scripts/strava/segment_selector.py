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

# activity_no = 13238398951
activity_no = 4069408520
activity_dict_list = {"activities": []}
stat_dict_list = {"stats": []}

activity = "https://www.strava.com/activities/" + str(activity_no)
driver.get(activity)
time.sleep(np.abs(np.random.randn()))


driver.find_elements(By.XPATH, '//*[@id="show-hidden-efforts"]')[0].click()


segment_tables = driver.find_elements(
    By.CSS_SELECTOR, ".dense.hoverable.marginless.segments"
)
segment_tables.append(
    driver.find_element(By.CSS_SELECTOR, ".dense.hidden-segments.hoverable.marginless")
)
time.sleep(1)
segment_no = []
segment_name = []
end_points = []
dict_list = []
for k, segment_table in enumerate(segment_tables):
    if k == 0:
        hidden = False
    else:
        hidden = True
    for j, segment in enumerate(segment_table.find_elements(By.TAG_NAME, "tr")):
        if j == 0 and k == 0:
            pass
        else:
            ends = []
            driver.execute_script(
                "arguments[0].click()", segment
            )  # This one is for clicking the element through Java as the usual way don't work on big screens
            time.sleep(4)
            clipper = driver.find_elements(By.CSS_SELECTOR, "[id^='view']")
            rects = clipper[0].find_elements(By.TAG_NAME, "rect")
            ends.append(float(rects[0].get_attribute("x")))
            ends.append(
                float(rects[0].get_attribute("x"))
                + float(rects[0].get_attribute("width"))
            )
            try:
                cat = (
                    segment.find_element(By.CSS_SELECTOR, "td.climb-cat-col")
                    .find_element(By.TAG_NAME, "span")
                    .get_attribute("title")
                )
            except NoSuchElementException:
                cat = None
                print("No category")

            segment_dict = {
                "activity_no": activity_no,
                "segment_no": segment.get_attribute("data-segment-effort-id"),
                "segment_name": segment.find_element(By.CSS_SELECTOR, "div.name").text,
                "end_points": ends,
                "category": cat,
                "hidden": hidden,
            }
            print(segment_dict)
            dict_list.append(segment_dict)
    print("-------hidden segments------")


json_string = json.dumps(dict_list)
with open(
    f"segments.json",
    "w",
) as f:
    f.write(json_string)

# driver.quit()
