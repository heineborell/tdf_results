import time

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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


df = pd.DataFrame(
    columns=["year", "date", "stage", "vertical_meters", "profile_score", "ps_25"]
)
i = 2009
driver.get(
    "https://www.procyclingstats.com/race/tour-de-france/" + str(i) + "/stage-11"
)

drop_list = driver.find_elements(By.CLASS_NAME, "pageSelectNav ")
year_element = drop_list[0].find_elements(By.TAG_NAME, "option")
stage_element = drop_list[1].find_elements(By.TAG_NAME, "option")
year_list = [year.text for year in year_element]
stage_list = [stage.text for stage in stage_element if "Stage" in stage.text]

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

    for time in time_table:
        time_lst.append(time.text)

    for j, _ in enumerate(time_lst):
        if time_lst[j] == ",,":
            time_lst[j] = time_lst[j - 1]

    info_lst = info_table.text.split("\n")
    print(info_lst)
    for i in info_lst:
        print(i.split(":"))

    info_dict = dict(zip(info_lst[0::2], info_lst[1::2]))

    df = pd.DataFrame({"name": name_lst, "time": time_lst[1:]})
    print(df)
    print(info_dict)
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
