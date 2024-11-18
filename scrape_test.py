import csv
import os
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
    time.sleep(3)

    # choose individual drop down
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

    ## choose stage dropdown
    # driver.find_element(
    #    By.XPATH,
    #    "//*[@id=" + str(year_lst[i]) + "]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]",
    # ).click()

    stages_dd = driver.find_element(By.ID, "stageSelect")
    stages = [
        stage.get_attribute("text")
        for stage in stages_dd.find_elements(By.TAG_NAME, "option")
    ]
    print(stages)
    for j in range(0, len(stages) - 18):
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
        time.sleep(4)

        the_soup = BeautifulSoup(driver.page_source, "html.parser")

        rankings = the_soup.find(
            "table", attrs={"class": "rankingTable rtable js-extend-target"}
        )
        riders = rankings.findChildren("tr")[1:]

        names = the_soup.find_all("td", attrs={"class": "runner"})

        name_lst = []
        for name in names:
            name_lst.append(name.text.strip())  # rider names

        print(name_lst)
        print(len(name_lst))

        timing_lst = []
        for rider in riders:
            timing_lst.append(
                rider.findChildren("td", attrs={"class": "is-alignCenter"})[1].text
            )  # riders attributes, index 1 is total time
        df = pd.DataFrame(
            {
                "year": [year_lst[i] for _ in range(1, len(names) + 1)],
                "stage": [stages[j] for _ in range(1, len(names) + 1)],
                "name": name_lst,
                "timing": timing_lst,
            }
        )
        print(df)

    # year counter
    i = i + 1

# for i in range(1, 5 + 1):
#    wait.until(
#        EC.presence_of_element_located(
#            (
#                By.XPATH,
#                "/html/body/div[2]/main/div[1]/section[1]/div/div[1]/div/div/div/div[1]/div",
#            )
#        )
#    )
#    year_dd.click()
#    year_xpath = "//html/body/div[2]/main/div[1]/section[1]/div/div[1]/div/div/div/div[1]/div/div[2]/"
#    year_xpath = year_xpath + "div" + str([i])
#    wait.until(EC.presence_of_element_located((By.XPATH, year_xpath)))
#    driver.find_element(By.XPATH, year_xpath).click()
#    time.sleep(2)

# year_val = year.get_attribute("text")
# year_lst.append(year_val)

# wait.until(
#    EC.presence_of_element_located(
#        (
#            By.XPATH,
#            "/html/body/div[2]/main/div[1]/section[1]/div/div[2]/div[111]/div[3]/div[2]/div[1]/div[1]/div[1]",
#        )
#    )
# )
# stage_dd = driver.find_element(
#    By.XPATH,
#    "/html/body/div[2]/main/div[1]/section[1]/div/div[2]/div[111]/div[3]/div[2]/div[1]/div[1]/div[1]",
# )
# stage_dd.click()
#
# wait.until(
#    EC.presence_of_element_located(
#        (
#            By.XPATH,
#            "/html/body/div[2]/main/div[1]/section[1]/div/div[2]/div[111]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]",
#        )
#    )
# )
# ind_dd = driver.find_element(
#    By.XPATH,
#    "/html/body/div[2]/main/div[1]/section[1]/div/div[2]/div[111]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]",
# )
# ind_dd.click()

# wait.until(
#    EC.presence_of_element_located(
#        (By.CSS_SELECTOR, ".select-selected.select-arrow-active")
#    )
# )

# stages_dd = driver.find_element(
#    "xpath", "//*[@id=2023]/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]"
# )

# stages_dd = wait.until(
#    EC.element_to_be_clickable(
#        driver.find_element(By.CSS_SELECTOR, ".select-selected.select-arrow-active")
#    )
# ).click()
# print(stages_dd)
# stages = stages_dd.find_elements(By.TAG_NAME, "div")
# print(len(stages))
# driver.implicitly_wait(10)
# print(stages[3].get_attribute("text"))


# stages_lst = []
# for stage in stages:
#    wait.until(EC.element_to_be_clickable(stage)).click()
#    driver.implicitly_wait(10)
#    stage_val = stage.get_attribute("text")
#    stages_lst.append(stage_val)
# print(stages_lst)

#
