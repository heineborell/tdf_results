import atexit
import getpass
import json
import sqlite3
from pathlib import Path

import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

from grand_tours import logger_config, segment_details

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

    stage_set = set()
    path = Path(
        f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segment_details/segment_details_{year}_{grand_tour}.json"
    )
    if path.exists():
        with open(path, "rb") as fp:  # Pickling
            tour_list = json.loads(fp.read())

        for item in tour_list:
            stage_set.add(item["stage"])
    else:
        tour_list = []

    print("Previously scraped", stage_set)
    logger = logger_config.setup_logger("segment.log")

    driver = uc.Chrome(
        user_data_dir="user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile 1",
        use_subprocess=True,
        version_main=133,
    )
    atexit.register(driver.quit)

    for i, item in enumerate(activity_no_list.values):
        if item[1] not in stage_set:
            print(item)
            wait = WebDriverWait(driver, 5)
            logger.info(f"------Stage-{i}, activity_no:{item[0]}")
            dict_list = segment_details.segment_details_scrape(item[0], f"{grand_tour}-{year}", item[1], driver)
            tour_list.extend(dict_list)

            json_string = json.dumps(tour_list)
            with open(
                f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/segment_details/segment_details_{year}_{grand_tour}.json",
                "w",
            ) as f:
                f.write(json_string)

    # driver.quit()
