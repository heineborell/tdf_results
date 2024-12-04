import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def activity_scraper(activity_id):
    service = Service()
    options = Options()
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    # options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(
        "user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile 1"
    )
    options.page_load_strategy = (
        "eager"  # Scraper doesn't wait for browser to load all the page
    )

    # Initialize Chrome with the specified options
    driver = webdriver.Chrome(service=service, options=options)
    activity = "https://www.strava.com/activities/" + str(activity_id)
    driver.get(activity)
    time.sleep(random.randint(1, 2))
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
    driver.quit()
    return [date, distance, name]
