import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Set up options for headless Chrome
options = Options()
# options.add_argument("--no-sandbox")
# options.add_argument("--headless")
# options.add_argument("--no-proxy-server")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-dev-shm-usage")
options.page_load_strategy = (
    "eager"  # Scraper doesn't wait for browser to load all the page
)
options.add_experimental_option("detach", True)

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

# use this to choose what year you want to scrape
year_list = year_list[108:]
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

    if "Stage 14 | Metz - Dunkerque" in stage_list:
        print("Stage 14 | Metz - Dunkerque seems to be wrong")
        stage_list.remove("Stage 14 | Metz - Dunkerque")
    else:
        pass

    if "Stage 4 | Grenoble - Toulon" in stage_list:
        print("Stage 4 | Grenoble - Toulon  taken out because of hour formatting")
        stage_list.remove("Stage 4 | Grenoble - Toulon")
    else:
        pass

    if "Stage 4 | Toulouse - Bordeaux" in stage_list:
        print("stage 4 | touoluse - bordeaux taken out because of hour formatting")
        stage_list.remove("Stage 4 | Toulouse - Bordeaux")

    if "Stage 16 | Tarbes - Pau" in stage_list:
        print("Stage 16 | Tarbes - Pau taken out because of tribute ride")
        stage_list.remove("Stage 16 | Tarbes - Pau")
    else:
        pass

    for i, stage in enumerate(stage_list):
        print(stage)
        driver.get(
            "https://www.procyclingstats.com/race/tour-de-france/"
            + year
            + "/stage-"
            + stage.split(" ")[1]
        )
        time.sleep(2)
        try:
            table = driver.find_element(
                By.CSS_SELECTOR, ".results.basic.moblist11"
            )  # this exception is for stages with relegations

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

            print(time_lst)
            ttt_val = 0
        except NoSuchElementException:

            try:
                ttt_test = driver.find_element(By.CLASS_NAME, "results-ttt")
                ttt_val = 1
            except NoSuchElementException:
                ttt_val = 0
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

                print(time_lst)
        if ttt_val == 0 and not all([el != ",," for el in time_lst]):

            for j, _ in enumerate(time_lst):

                if time_lst[j] != ",," and "-" not in time_lst[j]:
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
            print("If its normal the entries are empty if its not it is a TTT stage")

driver.quit()
