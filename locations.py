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
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--no-proxy-server")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-dev-shm-usage")
options.page_load_strategy = (
    "eager"  # Scraper doesn't wait for browser to load all the page
)
options.add_experimental_option("detach", True)

# Initialize Chrome with the specified options
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5)


df = pd.DataFrame()
page_list = range(1, 56)
print(page_list)

for page in page_list:
    print("page", page)
    driver.get("https://geokeo.com/database/town/fr/" + str(page) + "/")
    table = driver.find_element(By.CSS_SELECTOR, ".table.table-hover.table-bordered ")
    print(table)
    table_elements = table.find_elements(By.TAG_NAME, "tr")
    time.sleep(2)
    fr_table = []
    for i, element in enumerate(table_elements):
        first = element.text.split("France", 1)
        fisec = []

        if i == 0:
            pass  # fr_table.append(element.text.split(" "))
        else:
            fisec.extend(first[0].split(" ", 1))
            second = first[1].split(" ")[1:3]
            fr_table.append(fisec + second)

            print(fr_table)

# fr_dict = dict(
#     zip(np.array(fr_table)[0, :], [np.array(fr_table)[1:, k] for k in range(5)])
# )
# print(fr_dict)

# df = pd.concat(
#     [
#         df,
#         pd.DataFrame(fr_dict),
#     ]
# )
# df.to_csv("france_loc.csv")


driver.quit()
