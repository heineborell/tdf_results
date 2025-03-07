"""Module for scraping some segment details like endpoints, category"""

import json
import time
from pathlib import Path

import numpy as np
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def segment_details_scrape(activity_no: int, tour_year, stage: int, driver, username, year, grand_tour):
    path = Path(
        f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segment_details/segment_details_{year}_{grand_tour}.json"
    )
    if path.exists():
        with open(path, "rb") as fp:  # Pickling
            dict_list = json.loads(fp.read())
    else:
        dict_list = []
    activity = "https://www.strava.com/activities/" + str(activity_no)
    driver.get(activity)
    time.sleep(np.abs(np.random.randn()))

    prev_list = []
    for i in dict_list:
        prev_list.append([i["activity_no"], i["hidden"], i["segment_number"]])

    try:
        driver.find_elements(By.XPATH, '//*[@id="show-hidden-efforts"]')[0].click()
        segment_tables = driver.find_elements(By.CSS_SELECTOR, ".dense.hoverable.marginless.segments")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dense.hidden-segments.hoverable.marginless"))
        )
        segment_tables.append(driver.find_element(By.CSS_SELECTOR, ".dense.hidden-segments.hoverable.marginless"))
    except IndexError:
        print("No hidden segment")
        segment_tables = driver.find_elements(By.CSS_SELECTOR, ".dense.hoverable.marginless.segments")

    time.sleep(1)
    for k, segment_table in enumerate(segment_tables):
        if k == 0:
            hidden = False
        else:
            hidden = True
        for j, segment in enumerate(segment_table.find_elements(By.TAG_NAME, "tr")):
            if j == 0 and k == 0:
                pass
            elif [activity_no, hidden, j] in prev_list:
                pass
            else:
                ends = []
                driver.execute_script(
                    "arguments[0].click()", segment
                )  # This one is for clicking the element through Java as the usual way don't work on big screens
                time.sleep(4)
                clipper = driver.find_elements(By.CSS_SELECTOR, "[id^='view']")
                main_rect = driver.find_element(
                    By.XPATH,
                    '//*[@id="grid"]',
                )
                total_length = main_rect.find_element(By.TAG_NAME, "rect").get_attribute("width")
                rects = clipper[0].find_elements(By.TAG_NAME, "rect")
                ends.append(float(rects[0].get_attribute("x")))
                ends.append(float(rects[0].get_attribute("x")) + float(rects[0].get_attribute("width")))
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
                    "stage": stage,
                    "tour_year": tour_year,
                    "segment_no": segment.get_attribute("data-segment-effort-id"),
                    "segment_name": segment.find_element(By.CSS_SELECTOR, "div.name").text,
                    "end_points": ends,
                    "total_length": total_length,
                    "category": cat,
                    "hidden": hidden,
                    "segment_number": j,
                }
                print(segment_dict)
                dict_list.append(segment_dict)

                json_string = json.dumps(dict_list)
                with open(
                    f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segment_details/segment_details_{year}_{grand_tour}.json",
                    "w",
                ) as f:
                    f.write(json_string)

    return dict_list
