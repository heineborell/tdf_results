import getpass
import sqlite3
import time

import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == "__main__":
    username = getpass.getuser()
    conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db")

    grand_tour = "tdf"
    # grand_tour = "giro"
    year = 2022

    sql_list = f"""
    SELECT *
    FROM(
    SELECT
        ROW_NUMBER() OVER (
            PARTITION BY stage, tour_year
            ORDER BY ABS(strava_distance - avg_dist)
        ) AS strava_rank,
        activity_id,
        strava_distance,
        avg_dist,
        tour_year,
        stage
    FROM (
    SELECT *,
    AVG(strava_distance) OVER (PARTITION BY stage , tour_year) AS avg_dist
    FROM strava_table) t1)
    WHERE strava_rank = 1
      AND tour_year = '{grand_tour}-{year}'
    """
    activity_no_list = pd.read_sql_query(sql_list, conn)[["activity_id", "stage"]]

    driver = uc.Chrome(
        user_data_dir="user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile 3",
        use_subprocess=False,
        version_main=133,
    )
    print("activated driver")

    activity_no = 11768501612
    activity = "https://www.strava.com/activities/" + str(activity_no) + "/analysis "
    driver.get(activity)
    time.sleep(5)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="segmentBars"]')
        )  # Replace with a specific element for better accuracy
    )
    actions = ActionChains(driver)

    segments_chart = driver.find_element(By.XPATH, '//*[@id="segments-chart"]')
    segments_box = driver.find_element(By.XPATH, '//*[@id="segmentBars"]')

    segments = segments_box.find_elements(By.TAG_NAME, "rect")

    for rect_element in segments:
        # Get attributes
        x = rect_element.get_attribute("x")
        y = rect_element.get_attribute("y")
        width = rect_element.get_attribute("width")
        height = rect_element.get_attribute("height")
        class_name = rect_element.get_attribute("class")
        print(segments_chart.text)

        # Hover over the element
        actions.move_to_element(rect_element).perform()
        time.sleep(10)

        # Print the attributes
        print(f"x: {x}, y: {y}, width: {width}, height: {height}, class: {class_name}")

    driver.quit()
