import atexit
import getpass
import json
import sqlite3
from pathlib import Path

import pandas as pd
import undetected_chromedriver as uc

from grand_tours.segment_scraper import anal_scrape

if __name__ == "__main__":
    username = getpass.getuser()
    conn = sqlite3.connect(f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/grand_tours.db")

    grand_tour = "tdf"
    # grand_tour = "giro"
    year = 2024

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

    path = Path(
        f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/analysis/analysis_{year}_{grand_tour}.json"
    )
    if path.exists():
        with open(path, "rb") as f:  # Pickling
            json_data = json.loads(f.read())
        scraped_ids = {item["activity_id"] for item in json_data}
    else:
        json_data = []
        scraped_ids = {}

    for i, item in enumerate(activity_no_list.values):
        if item[0] in scraped_ids or i == 0 or i == 1 or i == 2 or i == 3:
            pass
        else:
            dict_list = anal_scrape(driver, item[0], item[1])
            json_data.extend(dict_list)
            print(json_data)
            json_string = json.dumps(json_data)
            print(json_string)
            with open(
                path,
                "w",
            ) as f:
                f.write(json_string)

    atexit.register(driver.quit)
