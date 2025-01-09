import json

import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine

import grand_tours
from grand_tours import chrome_driver, logger_config, segment_details

if __name__ == "__main__":

    engine = create_engine(
        "mysql+mysqldb://root:Abrakadabra69!@127.0.0.1:3306/grand_tours"
    )
    conn = engine.connect()

    grand_tour = "tdf"
    year = 2024

    sql_list = f"""SELECT * FROM ( SELECT ROW_NUMBER() OVER(PARTITION BY stage, year, tour ORDER BY ABS(dist_strava - avg_dist)) AS strava_rank, activity_id, dist_strava, avg_dist, tour, stage, year FROM ( SELECT *, AVG(dist_strava) OVER(PARTITION BY stage, year, tour) AS avg_dist FROM ( SELECT *, CAST(REGEXP_SUBSTR(`date`,'[0-9]{{4}}$') AS UNSIGNED) AS year FROM strava_table) t1) t2) ranked WHERE strava_rank = 1 and year= {year} and tour = 'tdf' """

    activity_no_list = pd.read_sql_query(sql_list, conn)["activity_id"].values.tolist()
    activity_no_list = [13071005082, 13238398951]

    logger = logger_config.setup_logger("segment.log")
    print(len(activity_no_list))

    tour_list = []
    for i, activity_no in enumerate(activity_no_list):
        driver = chrome_driver.start_driver(detach=False)
        wait = WebDriverWait(driver, 5)
        logger.info(f"------Stage-{i}, activity_no:{activity_no}")
        dict_list = segment_details.segment_details_scrape(activity_no, driver)
        tour_list.extend(dict_list)

        json_string = json.dumps(tour_list)
        with open(
            f"segment_details_{year}_{grand_tour}.json",
            "w",
        ) as f:
            f.write(json_string)
