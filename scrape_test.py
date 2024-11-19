import csv
import os
import re
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Set up options for headless Chrome
options = Options()
# options.headless = True  # Enable headless mode for invisible operation
options.add_argument("--window-size=1920,1200")  # Define the window size of the browser
options.add_experimental_option("detach", True)

# Initialize Chrome with the specified options
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)


driver.get("https://www.letour.fr/en/history")
driver.implicitly_wait(10)

wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))

driver.find_element(By.ID, "onetrust-accept-btn-handler").click()  # cookie accept

year_dd = driver.find_element(
    By.XPATH,
    "/html/body/div[2]/main/div[1]/section[1]/div/div[1]/div/div/div/div[1]/div",
)
year_options = driver.find_elements(
    By.XPATH,
    "//html/body/div[2]/main/div[1]/section[1]/div/div[1]/div/div/div/div[1]/div/div[2]/div",
)

year_len = len(year_options)

year_extr = driver.find_element(By.CSS_SELECTOR, ".custom-select.custom-select--year")
year_lst = [
    year.get_attribute("text")
    for year in year_extr.find_elements(By.TAG_NAME, "option")
]
print(year_lst)

i = 0
for year in year_options:
    print(year_lst[i])
    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[2]/main/div[1]/section[1]/div/div[1]/div/div/div/div[1]/div",
            )
        )
    )
    # choose year dropdown
    year_dd.click()
    # choose year
    year.click()
    time.sleep(2)

    # # choose individual drop down
    driver.find_element(
        By.XPATH,
        "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]",
    ).click()
    # individual select
    driver.find_element(
        By.XPATH,
        "//*[@id="
        + str(year_lst[i])
        + "]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]",
    ).click()
    time.sleep(2)

    # # choose stage dropdown
    # driver.find_element(
    #     By.XPATH,
    #     "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]",
    # ).click()

    stages_dd = driver.find_element(By.ID, "stageSelect")
    stages = [
        stage.get_attribute("text")
        for stage in stages_dd.find_elements(By.TAG_NAME, "option")
    ]
    print(stages)
    for j in range(0, len(stages) - 19):
        # choose stage
        print(j, "stage index")
        # again choose stage dropdown to choose new stage
        driver.find_element(
            By.XPATH,
            "//*[@id="
            + str(year_lst[i])
            + "]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]",
        ).click()
        driver.find_element(
            By.XPATH,
            "//*[@id="
            + str(year_lst[i])
            + "]/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/div"
            + str([j + 1]),
        ).click()
        time.sleep(2)

        ## next table rankings button this has to be in the stage loop
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[3]/a",
                )
            )
        )
        driver.find_element(
            By.XPATH, "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[3]/a"
        ).click()
        time.sleep(2)

        table = driver.find_element(
            By.XPATH,
            "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[2]/table",
        )
        cyclists = table.find_elements(By.TAG_NAME, "tr")
        ranking = np.zeros(3)
        for cyclist in cyclists:
            attrs = cyclist.find_elements(By.TAG_NAME, "td")
            attr_list = []
            for m, attr in enumerate(attrs):
                if m == 1 or m == 2 or m == 3:
                    attr_list.append(attr.text)
            if len(attr_list) == 3:
                ranking = np.vstack([ranking, attr_list])

        print(ranking)
    #
    # df = pd.DataFrame(
    #    {
    #        "year": [year_lst[i] for _ in range(1, len(names) + 1)],
    #        "stage": [stages[j] for _ in range(1, len(names) + 1)],
    #        "name": name_lst,
    #        "timing": timing_lst,
    #    }
    # )
    # print(df)

    # year counter
    # driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
    # driver.execute_script("scrollBy(0,450);")
    # time.sleep(2)
    html = driver.find_element(By.TAG_NAME, "html")
    html.send_keys(Keys.PAGE_UP)
    html.send_keys(Keys.PAGE_UP)
    html.send_keys(Keys.PAGE_UP)
    time.sleep(6)
    i = i + 1
