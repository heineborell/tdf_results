import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

service = Service()
# Set up options for headless Chrome
options = Options()
# options.headless = True  # Enable headless mode for invisible operation
# options.add_argument("--window-size=1920,1200")  # Define the window size of the browser
# options.add_experimental_option("detach", True)

# options.add_argument("--no-sandbox")
# options.add_argument("--headless")
# options.add_argument("--no-proxy-server")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(
    "user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile 1"
)
## options.add_argument("--disable-dev-shm-usage")
options.page_load_strategy = (
    "eager"  # Scraper doesn't wait for browser to load all the page
)

# Initialize Chrome with the specified options
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)
activity_no_list = [11888473406, 11888654604, 11879168103, 11878904744]
activity_dict_list = {"activities": []}
for activity_no in activity_no_list:
    activity = "https://www.strava.com/activities/" + str(activity_no)
    driver.get(activity)

    summary_container = driver.find_element(
        By.CSS_SELECTOR, ".row.no-margins.activity-summary-container"
    )
    summary_pre = summary_container.text.split("\n")[0].split(",")
    date = summary_pre[1] + " " + summary_pre[2].split(" ")[1]
    date = date.strip()
    distance = summary_container.text.split("\n")[
        summary_container.text.split("\n").index("Distance") - 1
    ].split(" ")[0]

    for i in driver.find_elements(By.XPATH, "//*[@id='heading']/header/h2/span/a"):
        name = i.get_attribute("href").split("/")[-1]

    activity_dict = {
        "activity_id": activity_no,
        "athlete_id": name,
        "date": date,
        "distance": distance,
        "segments": [],
    }

    segment_table = driver.find_element(
        By.CSS_SELECTOR, ".dense.hoverable.marginless.segments"
    )
    segment_name = []
    segment_distance = []
    segment_vert = []
    segment_grade = []
    segment_time = []
    segment_speed = []
    watt = []
    heart_rate = []
    VAM = []
    for segment in segment_table.find_elements(By.TAG_NAME, "tr"):
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
        "segment_name": segment_name,
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
    print(activity_dict)
    activity_dict_list["activities"].append(activity_dict)

json_string = json.dumps(activity_dict_list)
with open("segment.json", "w") as f:
    f.write(json_string)
# stats = driver.find_element(By.XPATH, '//*[@id="heading"]/div/div/div[2]')
# stat_list = stats.text.split("\n")
# stat_list.remove("Show More")
# print(stat_list)
driver.quit()
