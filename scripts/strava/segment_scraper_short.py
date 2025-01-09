import json
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
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqldb://root:Abrakadabra69!@127.0.0.1:3306/grand_tours")
conn = engine.connect()


# grand_tour = "giro"
grand_tour = "tdf"
year = 2024

service = Service()
# Set up options for headless Chrome
options = Options()
# options.add_experimental_option("detach", True)
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-proxy-server")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--blink-settings=imagesEnabled=false")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(
    "user-data-dir=/Users/dmini/Library/Application Support/Google/Chrome/Profile 1"
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


sql_list = """select p.activity,p.tour , p.date from( select  activity_id as activity,cast(REGEXP_SUBSTR(`date`, '[0-9]{4}$') as UNSIGNED) AS date, tour from strava_table where tour = 'tdf') as p where p.date=2024"""

activity_no_list = pd.read_sql_query(sql_list, conn)["activity"].values.tolist()
# last_index = activity_no_list.index("9406303142")
# activity_no_list = activity_no_list[last_index:]
print(len(activity_no_list))
activity_dict_list = {"activities": []}
stat_dict_list = {"stats": []}

for p, activity_no in enumerate(activity_no_list):
    activity = "https://www.strava.com/activities/" + str(activity_no)
    driver.get(activity)
    time.sleep(np.abs(np.random.randn()))

    # Extract the activity_type from the lightboxData JavaScript object
    # Find the script element containing pageProps
    script_element = driver.find_element(
        By.XPATH, "//script[contains(text(), 'pageProps')]"
    )

    # Get text content and parse activity_type
    script_text = script_element.get_attribute("innerHTML")
    activity_type = script_text.split('activity_type":"')[1].split('"')[0]
    print(activity_type)

    # Check if the activity type is 'Ride'
    if activity_type == "ride":
        print("Found ride activity type!")
    else:
        print("Ride activity type not found.")
        continue

    summary_container = driver.find_element(
        By.CSS_SELECTOR, ".row.no-margins.activity-summary-container"
    )
    summary_pre = summary_container.text.split("\n")[0].split(",")
    date = summary_pre[1] + " " + summary_pre[2].split(" ")[1]
    date = date.strip()
    try:
        distance = summary_container.text.split("\n")[
            summary_container.text.split("\n").index("Distance") - 1
        ].split(" ")[0]
    except ValueError:
        print("No Distance")

    for i in driver.find_elements(By.XPATH, "//*[@id='heading']/header/h2/span/a"):
        name = i.get_attribute("href").split("/")[-1]

    activity_dict = {
        "activity_id": activity_no,
        "athlete_id": name,
        "date": date,
        "distance": distance,
        "segments": [],
    }

    max_retries = 2  # Maximum number of retries (optional, for safety)
    retry_count = 0  # Track retries
    segment_tables = []

    if len(driver.find_elements(By.XPATH, '//*[@id="show-hidden-efforts"]')) != 0:
        while len(segment_tables) != 2:
            try:
                segment_tables = clicker(20)
            except TimeoutException:

                print("Timeout while waiting for the page to load. Reloading...")
                driver.refresh()  # Refresh the page
                segment_tables = clicker(20)
                retry_count += 1
                if retry_count >= max_retries:
                    print("Max retries reached. Exiting.")
                    break

            except NoSuchElementException:
                print("no segments")
                break
    else:
        print("No hidden segments.")
        segment_tables = driver.find_elements(
            By.CSS_SELECTOR, ".dense.hoverable.marginless.segments"
        )

    print(activity_no, f"{p}-{len(activity_no_list)}")
    segment_no = []
    segment_name = []
    segment_distance = []
    segment_vert = []
    segment_grade = []
    segment_time = []
    segment_speed = []
    watt = []
    heart_rate = []
    VAM = []
    for g, segment_table in enumerate(segment_tables):
        for m, segment in enumerate(segment_table.find_elements(By.TAG_NAME, "tr")):
            if m == 0 and g == 0:
                pass
            else:
                segment_no.append(segment.get_attribute("data-segment-effort-id"))
            for i, field in enumerate(segment.find_elements(By.TAG_NAME, "td")):
                if i == 3:
                    segment_name.append(field.text.split("\n")[0])
                    segment_distance.append(field.text.split("\n")[1].split(" ")[0])
                    segment_vert.append(field.text.split("\n")[1].split(" ")[2])
                    segment_grade.append(
                        field.text.split("\n")[1].split(" ")[4].split("%")[0]
                    )
                elif i == 5:
                    segment_time.append(field.text)
                elif i == 6:
                    segment_speed.append(field.text.split(" ")[0])
                elif i == 7:
                    watt.append(field.text.split(" ")[0])
                elif i == 8:
                    VAM.append(field.text)
                elif i == 9:
                    heart_rate.append(field.text.split("b")[0])

    segment_dict = {
        "segment_no": segment_no,
        "segment_time": segment_time,
        "segment_speed": segment_speed,
        "watt": watt,
        "heart_rate": heart_rate,
        "segment_distance": segment_distance,
        "segment_vert": segment_vert,
        "segment_grade": segment_grade,
        "VAM": VAM,
    }
    # activity_dict["activities"][0]['activity_id'].append(activity_no)
    activity_dict["segments"].append(segment_dict)
    activity_dict_list["activities"].append(activity_dict)

    try:
        stats = driver.find_element(By.XPATH, '//*[@id="heading"]/div/div/div[2]')
        stat_list = stats.text.split("\n")
        stat_list.remove("Show More")
        stat_dict = {}
        for i, stat in enumerate(stat_list):
            if stat == "Distance":
                stat_dict.update(
                    {
                        "activity_id": activity_no,
                        "athlete_id": name,
                        "dist": stat_list[i - 1],
                    }
                )
            if stat == "Moving Time":
                stat_dict.update({"move_time": stat_list[i - 1]})
            if stat == "Elevation":
                stat_dict.update({"elevation": stat_list[i - 1]})
            if stat == "Weighted Avg Power":
                stat_dict.update({"wap": stat_list[i - 1]})
            if stat == "total work":
                stat_dict.update({"tw": stat_list[i - 1]})
            if stat == "Avg Max":
                stat_dict.update({"avg_max": stat_list[i + 1]})
            if "Elapsed Time" in stat:
                stat_dict.update({"elapsed": stat_list[i].split(" ")[-1]})
            if stat == "Temperature":
                stat_dict.update({"temp": stat_list[i + 1]})
            if stat == "Humidity":
                stat_dict.update({"humd": stat_list[i + 1]})
            if stat == "Feels like":
                stat_dict.update({"feels": stat_list[i + 1]})
            if stat == "Wind Speed":
                stat_dict.update({"wind_speed": stat_list[i + 1]})
            if stat == "Wind Direction":
                stat_dict.update({"wind_direction": stat_list[i + 1]})
            if i == len(stat_list) - 1:
                stat_dict.update({"device": stat_list[i]})

        stat_dict_list["stats"].append(stat_dict)
    except ValueError:
        print("No more stat")

    json_string = json.dumps(activity_dict_list)
    with open(
        f"segment_{year}_{grand_tour}_short.json",
        "w",
    ) as f:
        f.write(json_string)
    json_string = json.dumps(stat_dict_list)
    with open(
        f"stat_{year}_{grand_tour}_short.json",
        "w",
    ) as f:
        f.write(json_string)
    time.sleep(3)


driver.quit()
