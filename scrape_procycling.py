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
for i in range(2001, 2025, 1):
    time.sleep(5)
    driver.get(
        "https://www.procyclingstats.com/race/tour-de-france/"
        + str(i)
        + "/route/stage-profiles"
    )

    time.sleep(2)
    stages = driver.find_elements(By.CLASS_NAME, "mt50")
    stage_table = np.zeros(5)
    for stage in stages:
        stage_lst = stage.text.split("\n")
        if len(stage_lst) == 10:
            stage_table = np.vstack([stage_table, stage_lst[1::2]])

    df = pd.concat(
        [
            df,
            pd.DataFrame(
                {
                    "year": i * np.ones(len(stage_table[:, 0])),
                    "date": stage_table[:, 0],
                    "stage": stage_table[:, 1],
                    "vertical_meters": stage_table[:, 2],
                    "profile_score": stage_table[:, 3],
                    "ps_25": stage_table[:, 4],
                }
            ).drop(index=0),
        ]
    )
    df.to_csv("procycling.csv")

    # driver.get(
#    "https://www.procyclingstats.com/race/tour-de-france/2023/route/stage-profiles"
# )
driver.quit()

# year_dd = driver.find_element(
#    By.XPATH,
#    "/html/body/div[3]/div[1]/div[1]/div[1]/div[1]/div/form/select",
# )
# year_options = driver.find_elements(
#    By.XPATH,
#    "/html/body/div[3]/div[1]/div[1]/div[1]/div[1]/div/form/select/option",
# )
# print(year_options)
# year_len = len(year_options)

# year_extr = driver.find_element(By.CSS_SELECTOR, ".custom-select.custom-select--year")
#
# year_lst = [
#    year.get_attribute("text")
#    for year in year_extr.find_elements(By.TAG_NAME, "option")
# ]
#
# df = pd.DataFrame(columns=["year", "stage", "name", "team_name", "timing"])

# i = 0
# for year in year_options:
#    wait.until(
#        EC.presence_of_element_located(
#            (
#                By.XPATH,
#                "/html/body/div[3]/div[1]/div[1]/div[1]/div[1]/div/form/select",
#            )
#        )
#    )
#    # choose year dropdown
#    year_dd.click()
#    # choose year
#    year.click()
#    print("year clicked")
#    time.sleep(2)
#
#    # # choose individual drop down
#    driver.find_element(
#        By.XPATH,
#        "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]",
#    ).click()
#    # individual select
#    driver.find_element(
#        By.XPATH,
#        "//*[@id="
#        + str(year_lst[i])
#        + "]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]",
#    ).click()
#    time.sleep(2)
#    print("individual clicked")
#
#    # # choose stage dropdown
#    # driver.find_element(
#    #     By.XPATH,
#    #     "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]",
#    # ).click()
#
#    stages_dd = driver.find_element(By.ID, "stageSelect")
#    stages = [
#        stage.get_attribute("text")
#        for stage in stages_dd.find_elements(By.TAG_NAME, "option")
#    ]
#    print(stages)
#    for j in range(0, len(stages)):
#        # choose stage
#        print(j, "stage index")
#        # again choose stage dropdown to choose new stage
#        driver.find_element(
#            By.XPATH,
#            "//*[@id="
#            + str(year_lst[i])
#            + "]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]",
#        ).click()
#        driver.find_element(
#            By.XPATH,
#            "//*[@id="
#            + str(year_lst[i])
#            + "]/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/div"
#            + str([j + 1]),
#        ).click()
#        time.sleep(2)
#        print("stage clicked")
#
#        ## next rankings button for the table
#        try:
#            wait.until(
#                EC.presence_of_element_located(
#                    (
#                        By.XPATH,
#                        "//*[@id="
#                        + str(year_lst[i])
#                        + "]/div[3]/div[2]/div[1]/div[3]/a",
#                    )
#                )
#            )
#        except TimeoutException:
#            print("couldnt find next ranking click")
#        else:
#            driver.find_element(
#                By.XPATH,
#                "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[3]/a",
#            ).click()
#            time.sleep(2)
#            print("next rankings clicked")
#
#        table = driver.find_element(
#            By.XPATH,
#            "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[2]/table",
#        )
#        cyclists = table.find_elements(By.TAG_NAME, "tr")
#        ranking = np.zeros(3)
#        for cyclist in cyclists:
#            attrs = cyclist.find_elements(By.TAG_NAME, "td")
#            attr_list = []
#            for m, attr in enumerate(attrs):
#                if m == 1 or m == 2 or m == 3:
#                    attr_list.append(attr.text)
#            if len(attr_list) == 3:
#                ranking = np.vstack([ranking, attr_list])
#
#        try:
#            name_lst = ranking[:, 0]
#            team_lst = ranking[:, 1]
#            timing_lst = ranking[:, 2]
#        except IndexError:
#            print("the ranking table is empty or some other index problem")
#        else:
#
#            df = pd.concat(
#                [
#                    df,
#                    pd.DataFrame(
#                        {
#                            "year": [
#                                year_lst[i] for _ in range(1, ranking.shape[0] + 1)
#                            ],
#                            "stage": [
#                                stages[j] for _ in range(1, ranking.shape[0] + 1)
#                            ],
#                            "name": name_lst,
#                            "team_name": team_lst,
#                            "timing": timing_lst,
#                        }
#                    ).drop(index=0),
#                ]
#            )
#            df.to_csv("TDF_2.csv")
#
#    html = driver.find_element(By.TAG_NAME, "html")
#    html.send_keys(Keys.PAGE_UP)
#    html.send_keys(Keys.PAGE_UP)
#    html.send_keys(Keys.PAGE_UP)
#    time.sleep(6)
#    i = i + 1
