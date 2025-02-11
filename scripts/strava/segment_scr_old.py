import gzip
import pickle
import time

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# grand_tour = "giro"
grand_tour = "tdf"
year = 2012

service = Service()
# Set up options for headless Chrome
options = Options()
options.add_experimental_option("detach", True)
# options.add_argument("--no-sandbox")
# options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-proxy-server")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--blink-settings=imagesEnabled=false")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(
    "user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile 1"
)
## options.add_argument("--disable-dev-shm-usage")
# options.page_load_strategy = (
#    "eager"  # Scraper doesn't wait for browser to load all the page
# )

# Initialize Chrome with the specified options
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)


def clicker(wait_time):

    driver.find_elements(By.XPATH, '//*[@id="show-hidden-efforts"]')[0].click()

    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    tables = driver.find_elements(
        By.CSS_SELECTOR, ".dense.hoverable.marginless.segments"
    )
    WebDriverWait(driver, wait_time).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".dense.hidden-segments.hoverable.marginless")
        )
    )
    tables.append(
        driver.find_element(
            By.CSS_SELECTOR, ".dense.hidden-segments.hoverable.marginless"
        )
    )

    return tables


activity_no_list = (
    pd.read_csv(
        f"~/iCloud/Research/Data_Science/Projects/data/strava/activity_list/activity_list_{grand_tour}_{year}.csv"
    )
    .drop_duplicates(subset=["activity"])["activity"]
    .values.tolist()
)

activity_no_list = [659892658]
print(len(activity_no_list))
activity_main_list = []
for p, activity_no in enumerate(activity_no_list):
    activity_big_list = []
    activity = "https://www.strava.com/activities/" + str(activity_no)
    driver.get(activity)
    time.sleep(np.abs(np.random.randn()))

    # Extract the activity_type from the lightboxData JavaScript object
    # Find the script element containing pageProps
    script_element = driver.find_element(
        By.XPATH, "//script[contains(text(), 'pageProps')]"
    )

    # Get text content and parse activity_type
    try:
        script_text = script_element.get_attribute("innerHTML")
        activity_type = script_text.split('activity_type":"')[1].split('"')[0]
        activity_big_list.append([[activity_no], [activity_type]])
        print(activity_type)
    except (NoSuchElementException, AttributeError):
        activity_big_list.append(
            [
                [activity_no],
                ["no activity type"],
                [],
                [],
                [],
                [],
            ]
        )
        print("no activity type")

        activity_main_list.append(activity_big_list)
        with gzip.open(f"segment_{year}_{grand_tour}.pkl.gz", "wb") as fp:  # Pickling
            pickle.dump(activity_main_list, fp)

        continue

    # Check if the activity type is 'Ride' if not skip this activity
    if activity_type == "ride":
        print("Found ride activity type!")
    else:
        activity_big_list[0].extend(
            [
                [],
                [],
                [],
                [],
            ]
        )
        print(f"{activity_type} activity type found.")
        print(activity_big_list)
        activity_main_list.append(activity_big_list)
        with gzip.open(f"segment_{year}_{grand_tour}.pkl.gz", "wb") as fp:  # Pickling
            pickle.dump(activity_main_list, fp)

        continue

    # Get the summary container if it exists
    try:
        summary_container = driver.find_element(
            By.CSS_SELECTOR, ".row.no-margins.activity-summary-container"
        )
        activity_big_list[0].append([summary_container.text])
    except NoSuchElementException:
        activity_big_list[0].append(["No summary container"])
        print("No summary container")

    # Get the athlete id
    try:
        for i in driver.find_elements(By.XPATH, "//*[@id='heading']/header/h2/span/a"):
            print(i.get_attribute("href"))
            name = i.get_attribute("href").split("/")[-1]
            activity_big_list[0].append([name])
    except NoSuchElementException:
        activity_big_list[0].append(["no athelete_id!"])
        print("no athelete_id!")

    max_retries = 2  # Maximum number of retries (optional, for safety)
    retry_count = 0  # Track retries
    segment_tables = []

    # First look for hidden segments then push save the segment tables as html to parse with beatiful soup
    if len(driver.find_elements(By.XPATH, '//*[@id="show-hidden-efforts"]')) != 0:
        while len(segment_tables) != 2:
            try:
                segment_tables = clicker(20)
                segment_tables = [i.get_attribute("innerHTML") for i in segment_tables]
            except TimeoutException:

                print("Timeout while waiting for the page to load. Reloading...")
                driver.refresh()  # Refresh the page
                segment_tables = clicker(20)
                segment_tables = [i.get_attribute("innerHTML") for i in segment_tables]
                retry_count += 1
                if retry_count >= max_retries:
                    print("Max retries reached. Exiting.")
                    break

            except NoSuchElementException:
                print("no segments")
                activity_big_list[0].append(["no segments"])
                break
    else:
        print("No hidden segments.")
        segment_tables = driver.find_elements(
            By.CSS_SELECTOR, ".dense.hoverable.marginless.segments"
        )
        segment_tables = [i.get_attribute("innerHTML") for i in segment_tables]

    activity_big_list[0].append(segment_tables)

    print(activity_no, f"{p}-{len(activity_no_list)}")

    # Finally look for more stats and if it exists save
    try:
        stats = driver.find_element(By.XPATH, '//*[@id="heading"]/div/div/div[2]')
        stat_list = stats.text.split("\n")
        activity_big_list[0].append(stat_list)
    except ValueError:
        activity_big_list[0].append(["No more stat!"])
        print("No more stat")

    activity_main_list.append(activity_big_list)
    with gzip.open(f"segment_{year}_{grand_tour}.pkl.gz", "wb") as fp:  # Pickling
        pickle.dump(activity_main_list, fp)

    time.sleep(3)


driver.quit()
