import getpass
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def ride_scraper(pro_id, date):
    username = getpass.getuser()
    # Initialize Chrome with the specified options
    service = Service()
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-proxy-server")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--blink-settings=imagesEnabled=false")
    # options.add_experimental_option("detach", True)
    options.add_argument(
        f"user-data-dir=/Users/{username}/Library/Application Support/Google/Chrome/Profile 1"
    )

    driver = webdriver.Chrome(service=service, options=options)
    homepage = (
        "https://www.strava.com/pros/"
        + str(pro_id)
        + "#interval?interval="
        + str(date)
        + "&interval_type=week&chart_type=miles&year_offset=0"
    )
    driver.get(homepage)
    time.sleep(13)
    activities = []
    for m in driver.find_elements(By.CSS_SELECTOR, "a[data-testid='activity_name']"):
        activities.append(m.get_attribute("href").split("/")[-1])
    driver.quit()
    return activities
