import getpass
import json
import sqlite3

import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

from grand_tours import logger_config, segment_details

if __name__ == "__main__":
    username = getpass.getuser()
    conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db")

    grand_tour = "tdf"
    year = 2018

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

    logger = logger_config.setup_logger("segment.log")

    tour_list = []
    for i, item in enumerate(activity_no_list.values):
        print(item)
        driver = uc.Chrome(
            user_data_dir="user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile 1",
            use_subprocess=True,
            version_main=132,
        )

        wait = WebDriverWait(driver, 5)
        logger.info(f"------Stage-{i}, activity_no:{item[0]}")
        dict_list = segment_details.segment_details_scrape(item[0], f"{grand_tour}-{year}", item[1], driver)
        tour_list.extend(dict_list)

        json_string = json.dumps(tour_list)
        with open(
            f"segment_details_{year}_{grand_tour}.json",
            "w",
        ) as f:
            f.write(json_string)

    driver.quit()
