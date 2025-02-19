"""This is for scraping the rides from week page of a rider. Basically populates the activity_list!"""

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
    options.add_argument(f"user-data-dir=/Users/{username}/Library/Application Support/Google/Chrome/Profile 1")

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


def wait_for_page_activity_to_stop(driver, timeout=10, check_interval=0.5):
    prev_html = driver.page_source
    end_time = time.time() + timeout
    while time.time() < end_time:
        time.sleep(check_interval)
        new_html = driver.page_source
        if new_html == prev_html:
            return True  # Page has stabilized
        prev_html = new_html
    return False  # Timeout reached


def ride_scraper_local(pro_id, date):
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
    options.add_argument("--blink-settings=imagesEnabled=true")
    # options.add_experimental_option("detach", True)
    options.add_argument(f"user-data-dir=/Users/{username}/Library/Application Support/Google/Chrome/Profile 1")

    driver = webdriver.Chrome(service=service, options=options)
    homepage = (
        "https://www.strava.com/pros/"
        + str(pro_id)
        + "#interval?interval="
        + str(date)
        + "&interval_type=week&chart_type=miles&year_offset=0"
    )
    driver.get(homepage)
    # wait_for_page_activity_to_stop(driver)
    time.sleep(15)
    # WebDriverWait(driver, 15).until(
    #     EC.presence_of_element_located((By.TAG_NAME, "body"))  # Replace with a specific element for better accuracy
    # )
    activities = []
    panes = driver.find_elements(By.XPATH, '//*[@id="feed-entry-null"]/div')
    print(date, len(panes))
    for pane in panes:
        activity_list = pane.find_elements(By.CSS_SELECTOR, "a[data-testid='activity_name']")
        try:
            activities.append(activity_list[0].get_attribute("href").split("/")[-1])
        except IndexError:
            print("sth wrong with pane")
            continue
    driver.quit()
    print(f"for athlete {pro_id}-{activities}")
    return activities
