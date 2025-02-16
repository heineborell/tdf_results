"""This script is for to scrape the city coordinates in France"""

import re
import time

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Set up options for headless Chrome
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--no-proxy-server")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-dev-shm-usage")
options.page_load_strategy = "eager"  # Scraper doesn't wait for browser to load all the page
options.add_experimental_option("detach", True)

# Initialize Chrome with the specified options
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5)


# Find all matches

df = pd.DataFrame(columns=["place_name", "coordinate_x", "coordinate_y"])
page_list = range(1, 56)

for page in page_list:
    print("page", page)
    driver.get("https://geokeo.com/database/town/fr/" + str(page) + "/")
    table = driver.find_element(By.CSS_SELECTOR, ".table.table-hover.table-bordered ")
    table_elements = table.find_elements(By.TAG_NAME, "tr")
    time.sleep(2)
    fr_table = []
    pattern = r"\b\d+\s([\w\s]+)"
    for i, element in enumerate(table_elements):
        first = element.text.split("France", 1)
        matches = re.findall(pattern, first[0])

        if i == 0:
            pass  # fr_table.append(element.text.split(" "))
        else:
            second = first[1].split(" ")[1:3]
            fr_table.append(matches + second)

    print(fr_table)
    # fr_dict = dict(
    #    zip(np.array(fr_table)[0, :], [np.array(fr_table)[1:, k] for k in range(3)])
    # )

    df = pd.concat(
        [
            df,
            pd.DataFrame(
                {
                    "place_name": np.array(fr_table)[:, 0],
                    "coordinate_x": np.array(fr_table)[:, 1],
                    "coordinate_y": np.array(fr_table)[:, 2],
                }
            ),
        ]
    )
    df.to_csv("france_loc.csv")


driver.quit()
