import time
from datetime import datetime, timedelta

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def setup_driver():
    """Set up the Selenium WebDriver with specified options."""
    options = Options()
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-dev-shm-usage")
    options.page_load_strategy = "eager"  # Don't wait for full page load
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    return driver


def get_years(driver):
    """Retrieve the list of available years for the race."""
    year_dropdown = driver.find_elements(By.CLASS_NAME, "pageSelectNav ")[0]
    year_elements = year_dropdown.find_elements(By.TAG_NAME, "option")
    years = [year.text for year in year_elements][1:]  # Exclude default option
    return years


def get_stages(driver, year):
    """Retrieve the list of stages for a given year."""
    driver.get(f"https://www.procyclingstats.com/race/tour-de-france/{year}/")
    stage_dropdowns = driver.find_elements(By.CLASS_NAME, "pageSelectNav ")
    stage_index = 1 if len(stage_dropdowns) == 2 else 2
    stage_elements = stage_dropdowns[stage_index].find_elements(By.TAG_NAME, "option")
    stages = [stage.text for stage in stage_elements if "Stage" in stage.text]
    return stages


def clean_stages(stages):
    """Remove problematic stages based on known issues."""
    exclusions = [
        "Stage 14 | Metz - Dunkerque",
        "Stage 4 | Grenoble - Toulon",
        "Stage 4 | Toulouse - Bordeaux",
    ]
    return [stage for stage in stages if stage not in exclusions]


def parse_time(time_str):
    """Convert a time string into total seconds."""
    try:
        if time_str and "," not in time_str:
            t = (
                datetime.strptime(time_str, "%H:%M:%S")
                if ":" in time_str
                else datetime.strptime(time_str, "%M:%S")
            )
        else:
            t = datetime.strptime(time_str.split(",")[0], "%M.%S")
        return int(
            timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
        )
    except ValueError:
        return None


def scrape_stage(driver, year, stage):
    """Scrape data for a specific stage."""
    url = f"https://www.procyclingstats.com/race/tour-de-france/{year}/stage-{stage.split(' ')[1]}"
    driver.get(url)
    time.sleep(2)
    try:

        table = driver.find_element(By.CSS_SELECTOR, ".results.basic.moblist11")
        rows = table.find_elements(By.TAG_NAME, "tr")
        times = [
            parse_time(row.find_element(By.CSS_SELECTOR, ".time.ar").text)
            for row in rows[1:]
        ]
        names = [
            row.text.split("\n")[1] for row in rows if len(row.text.split("\n")) > 2
        ]
        return names, times
    except NoSuchElementException:
        print("No relagations")

    try:
        driver.find_element(By.CLASS_NAME, "results-ttt")
        print(f"Stage {stage} is a TTT stage.")
        return None, None
    except NoSuchElementException:
        table = driver.find_element(By.CSS_SELECTOR, ".results.basic.moblist10")
        rows = table.find_elements(By.TAG_NAME, "tr")
        times = [
            parse_time(row.find_element(By.CSS_SELECTOR, ".time.ar").text)
            for row in rows[1:]
        ]
        names = [
            row.text.split("\n")[1] for row in rows if len(row.text.split("\n")) > 2
        ]
        return names, times


def main():
    driver = setup_driver()
    driver.get("https://www.procyclingstats.com/race/tour-de-france/2024/stage-11")

    df = pd.DataFrame(columns=["year", "stage", "name", "time"])
    years = get_years(driver)
    print("Available years:", years)

    for year in years:
        print(f"Scraping year {year}...")
        stages = get_stages(driver, year)
        stages = clean_stages(stages)
        for stage in stages:
            print(f"Scraping {stage}...")
            names, times = scrape_stage(driver, year, stage)
            if names and times:
                stage_data = {
                    "year": [int(year)] * len(names),
                    "stage": [stage] * len(names),
                    "name": names,
                    "time": times,
                }
                df = pd.concat([df, pd.DataFrame(stage_data)], ignore_index=True)

    df.to_csv("protdf.csv", index=False)
    print("Scraping complete. Data saved to 'protdf.csv'.")
    driver.quit()


if __name__ == "__main__":
    main()
