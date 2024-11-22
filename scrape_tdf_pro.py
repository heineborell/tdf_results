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
info_element = info_table.find_elements(By.TAG_NAME, "li")
info_lst = info_table.text.split("\n")

info_lst = [info.text for info in info_element]
final_info_lst = []
for i in info_lst:
    if len(i.split("\n")) == 1:
        single_el = i.split("\n")
        single_el.append("EMPTY")
        final_info_lst.append(single_el)
    else:
        final_info_lst.append(i.split("\n"))

final_info_lst = np.array(final_info_lst).flatten()
info_dict = dict(zip(final_info_lst[0::2], final_info_lst[1::2]))
info_df = pd.DataFrame(columns=list(info_dict.keys()))

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
            info_element = info_table.find_elements(By.TAG_NAME, "li")
            name_lst = []
            time_lst = []

            for rank in rank_lst:
                if len(rank.text.split("\n")) > 2:
                    name_lst.append(rank.text.split("\n")[1])

            for k, t in enumerate(time_table):
                if k > 0:
                    time_lst.append(t.text)

            for j, _ in enumerate(time_lst):

                if time_lst[j] != ",," and time_lst[j] != "-":
                    try:
                        t = datetime.strptime(time_lst[j], "%H:%M:%S")
                        time_lst[j] = int(
                            timedelta(
                                hours=t.hour, minutes=t.minute, seconds=t.second
                            ).total_seconds()
                        )

                    except ValueError:
                        if "," not in time_lst[j]:
                            t = datetime.strptime(time_lst[j], "%M:%S")
                            time_lst[j] = int(
                                timedelta(
                                    hours=t.hour, minutes=t.minute, seconds=t.second
                                ).total_seconds()
                            )
                        else:
                            stripped_t = time_lst[j][0 : time_lst[j].index(",")]
                            t = datetime.strptime(stripped_t, "%M.%S")
                            time_lst[j] = int(
                                timedelta(
                                    hours=t.hour, minutes=t.minute, seconds=t.second
                                ).total_seconds()
                            )

            for j, _ in enumerate(time_lst):
                if isinstance(time_lst[j], int) and j > 0:
                    time_lst[j] = time_lst[j] + time_lst[0]

            for j, _ in enumerate(time_lst):
                if time_lst[j] == ",,":
                    time_lst[j] = time_lst[j - 1]

            info_lst = [info.text for info in info_element]
            final_info_lst = []
            for i in info_lst:
                if len(i.split("\n")) == 1:
                    single_el = i.split("\n")
                    single_el.append("Na")
                    final_info_lst.append(single_el)
                else:
                    final_info_lst.append(i.split("\n"))

            final_info_lst = np.array(final_info_lst).flatten()

            # construct info table dictionary
            info_dict = dict(zip(final_info_lst[0::2], final_info_lst[1::2]))
            info_dict = {
                k: [v] for k, v in info_dict.items()
            }  # this is needed as pandas want and index (kinda hack solution)
            info_df = pd.concat(
                [info_df, pd.DataFrame.from_dict(info_dict)], ignore_index=True
            )
            final_dict = {
                "year": [int(year)] * len(name_lst),
                "stage": [stage] * len(name_lst),
                "name": name_lst,
                "time": time_lst,
            }
            info_dict_ext = {k: v * len(name_lst) for k, v in info_dict.items()}
            final_dict = final_dict | info_dict_ext

            df = pd.concat(
                [
                    df,
                    pd.DataFrame(final_dict),
                ]
            )
            df.to_csv("protdf.csv")
            info_df.to_csv("infodf.csv")
        else:
            print("It is a TTT stage")

driver.quit()
