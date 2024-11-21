import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Set up options for headless Chrome
options = Options()
options.headless = True  # Enable headless mode for invisible operation
options.add_argument("--window-size=1920,1200")  # Define the window size of the browser
options.page_load_strategy = "eager"
# options.add_experimental_option("detach", True)

# Initialize Chrome with the specified options
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5)


driver.get("https://www.procyclingstats.com/race/tour-de-france/2024/stage-11")


df = pd.DataFrame(columns=["year", "stage", "name", "time"])
table = driver.find_element(By.CSS_SELECTOR, ".results.basic.moblist10")
info_table = driver.find_element(By.CSS_SELECTOR, ".infolist")
info_lst = info_table.text.split("\n")
info_dict = dict(zip(info_lst[0::2], info_lst[1::2]))
info_df = pd.DataFrame(columns=list(info_dict.keys()))
print()

drop_list = driver.find_elements(By.CLASS_NAME, "pageSelectNav ")
year_element = drop_list[0].find_elements(By.TAG_NAME, "option")
year_list = [year.text for year in year_element]
del year_list[0]
print(year_list)

for year in year_list:
    print(year)
    driver.get("https://www.procyclingstats.com/race/tour-de-france/" + year + "/")
    drop_list = driver.find_elements(By.CLASS_NAME, "pageSelectNav ")
    time.sleep(2)
    if len(drop_list) == 2:
        stage_element = drop_list[1].find_elements(By.TAG_NAME, "option")
        stage_list = [stage.text for stage in stage_element if "Stage" in stage.text]
    elif len(drop_list) == 3:
        stage_element = drop_list[2].find_elements(By.TAG_NAME, "option")
        stage_list = [stage.text for stage in stage_element if "Stage" in stage.text]

    for i, stage in enumerate(stage_list):
        print(stage)
        driver.get(
            "https://www.procyclingstats.com/race/tour-de-france/"
            + year
            + "/stage-"
            + str(i + 1)
        )
        time.sleep(2)

        try:
            ttt_test = driver.find_element(By.CLASS_NAME, "results-ttt")
        except NoSuchElementException:
            print("It is a normal stage.")
            table = driver.find_element(By.CSS_SELECTOR, ".results.basic.moblist10")

            rank_lst = table.find_elements(By.TAG_NAME, "tr")
            time_table = table.find_elements(By.CSS_SELECTOR, ".time.ar")
            info_table = driver.find_element(By.CSS_SELECTOR, ".infolist")
            name_lst = []
            time_lst = []

            for rank in rank_lst:
                if len(rank.text.split("\n")) > 2:
                    name_lst.append(rank.text.split("\n")[1])

            for t in time_table:
                time_lst.append(t.text)

            for j, _ in enumerate(time_lst):

                if j > 0 and time_lst[j] != ",," and time_lst[j] != "-":
                    try:
                        t = datetime.strptime(time_lst[j], "%H:%M:%S")
                        time_lst[j] = timedelta(
                            hours=t.hour, minutes=t.minute, seconds=t.second
                        ).total_seconds()

                    except ValueError:
                        t = datetime.strptime(time_lst[j], "%M:%S")
                        time_lst[j] = timedelta(
                            hours=t.hour, minutes=t.minute, seconds=t.second
                        ).total_seconds()

            # for j, _ in enumerate(time_lst):
            #     if time_lst[j] == ",,":
            #         time_lst[j] = time_lst[j - 1]

            info_lst = info_table.text.split("\n")

            info_dict = dict(zip(info_lst[0::2], info_lst[1::2]))
            # info_df = pd.concat([info_df, pd.DataFrame(info_dict)], ignore_index=True)
            # info_df = pd.DataFrame(info_dict)

            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        {
                            "year": [int(year)] * len(name_lst),
                            "stage": [stage] * len(name_lst),
                            "name": name_lst,
                            "time": time_lst[1:],
                        }
                    ),
                ]
            )
            df.to_csv("protdf.csv")
            info_df.to_csv("infodf.csv")
        else:
            print("It is a TTT stage")
# for key in list(info_dict.keys()):
# print(key)
# if len(stage_lst) == 10:
#  stage_table = np.vstack([stage_table, stage_lst[1::2]])

# for i in range(2001, 2025, 1):
#    time.sleep(5)
#    driver.get(
#        "https://www.procyclingstats.com/race/tour-de-france/"
#        + str(i)
#        + "/route/stage-profiles"
#    )
#
#    time.sleep(2)
#    stages = driver.find_elements(By.CLASS_NAME, "mt50")
#    stage_table = np.zeros(5)
#    for stage in stages:
#        stage_lst = stage.text.split("\n")
#        if len(stage_lst) == 10:
#            stage_table = np.vstack([stage_table, stage_lst[1::2]])
#
#    df = pd.concat(
#        [
#            df,
#            pd.DataFrame(
#                {
#                    "year": i * np.ones(len(stage_table[:, 0])),
#                    "date": stage_table[:, 0],
#                    "stage": stage_table[:, 1],
#                    "vertical_meters": stage_table[:, 2],
#                    "profile_score": stage_table[:, 3],
#                    "ps_25": stage_table[:, 4],
#                }
#            ).drop(index=0),
#        ]
#    )
#    df.to_csv("procycling.csv")
#
#    # driver.get(
##    "https://www.procyclingstats.com/race/tour-de-france/2023/route/stage-profiles"
## )
# driver.quit()
