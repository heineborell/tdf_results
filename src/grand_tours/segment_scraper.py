import concurrent.futures
import json
import os
import threading
import time

import numpy as np
import pandas as pd
import undetected_chromedriver as uc
from dotenv import load_dotenv
from rich import print as rprint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine

import grand_tours
from grand_tours import chrome_driver, chrome_driver_stealth, chrome_grid_driver


class SegmentScrape:
    def __init__(
        self, grand_tour: str, year: int, activity_whole_list, max_workers
    ) -> None:
        self.grand_tour = grand_tour
        self.year = year
        self.max_workers = max_workers
        self.activity_whole_list = activity_whole_list
        print(len(activity_whole_list))
        self.activity_whole_list = self._split_into_n(
            self.activity_whole_list, self.max_workers
        )

    def _split_into_n(self, lst, n):
        avg_size = len(lst) // n
        remainder = len(lst) % n
        sublists = []
        start = 0
        for i in range(n):
            end = start + avg_size + (1 if i < remainder else 0)
            sublists.append(lst[start:end])
            start = end
        return sublists

    def _clicker(self, driver, wait_time):

        driver.find_elements(By.XPATH, '//*[@id="show-hidden-efforts"]')[0].click()

        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
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

    def _load_page_with_retry(self, driver, url, max_retries=5):
        retries = 0
        while retries < max_retries:
            try:
                rprint(
                    f"[bold yellow] Attempt {retries + 1}: Trying to load URL: {url}[/bold yellow]"
                )
                driver.execute_script(
                    "Object.defineProperty(navigator, 'webdrier', {get: () => undefined})"
                )
                driver.get(url)

                # Wait for a specific element to confirm page load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, "body")
                    )  # Replace with a specific element for better accuracy
                )
                rprint("[bold green] Page loaded successfully! [/bold green]")
                time.sleep(np.abs(np.random.randn()))
                break  # Exit the loop if the page loads successfully
            except TimeoutException:
                retries += 1
                rprint(
                    f"[bold red] Retry {retries}/{max_retries}: Page did not load completely. Retrying...[/bold red]"
                )
                time.sleep(3)  # Optional wait before retrying
        else:
            rprint(
                "[bold red] Max retries reached. Could not load the page. [/bold red]"
            )

    def segment_scraper(self):
        print(self.activity_whole_list)
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            futures = {
                executor.submit(self._activity_data_getter, i + 1, j): j
                for i, j in enumerate(self.activity_whole_list)
            }

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    rprint(f"[turquoise2] Task result:{result} [/turquoise2]")
                except Exception as e:
                    task_id = futures[future]
                    rprint(
                        f"[bright red] Task {task_id} generated an exception: {e} [/bright red]"
                    )

    def _strava_login(self, driver, email, password):

        print(email)
        print(password)
        driver.delete_all_cookies()
        # open strava
        driver.get("https://www.strava.com")

        # Give the browser time to load all content.
        time.sleep(5)

        # click login button
        driver.find_element(
            By.XPATH, '//*[@id="__next"]/div[2]/div[1]/nav/div/div[1]/div[2]/button'
        ).click()

        time.sleep(5)

        # click cookies button
        driver.find_element(
            By.XPATH, ' //*[@id="__next"]/div[1]/div/div/button[1] '
        ).click()

        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located(
        #         (
        #             By.XPATH,
        #             '//*[@id="__next"]/div[2]/div[1]/nav/div/div[1]/div[2]/button',
        #         )
        #     )
        # )
        # click don't remember me
        driver.find_element(
            By.XPATH,
            '//*[@id="__next"]/div/div[2]/div[2]/div/div[2]/form/div[3]/label',
        ).click()
        time.sleep(5)

        # enter email
        driver.find_element(By.XPATH, '//*[@id="desktop-email"]').send_keys(f"{email}")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="desktop-login-button"]'))
        )
        # click first login for email
        driver.find_element(By.XPATH, '//*[@id="desktop-login-button"]').click()
        time.sleep(5)

        # enter password
        driver.find_element(
            By.XPATH,
            '//*[@id="__next"]/div/div[2]/div[2]/div/div/form/div[1]/div[2]/div/input',
        ).send_keys(f"{password}")

        time.sleep(5)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="__next"]/div/div[2]/div[2]/div/div/form/div[2]/button',
                )
            )
        )
        driver.find_element(
            By.XPATH,
            '//*[@id="__next"]/div/div[2]/div[2]/div/div/form/div[2]/button',
        ).click()

        time.sleep(5)

    def _activity_data_getter(self, account_no, activity_no_list):
        print(f"for the account no {account_no} we have the table {activity_no_list}")
        thread_id = threading.get_ident()
        activity_dict_list = {"activities": []}
        stat_dict_list = {"stats": []}
        driver = uc.Chrome(use_subprocess=True)
        load_dotenv()
        self._strava_login(
            driver,
            os.getenv(f"STRAVA_EMAIL_{account_no}"),
            os.getenv(f"STRAVA_PASSWORD_{account_no}"),
        )

        for p, activity_no in enumerate(activity_no_list):
            activity = "https://www.strava.com/activities/" + str(activity_no)
            driver.get(activity)
            # self._load_page_with_retry(driver, activity)

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

            for i in driver.find_elements(
                By.XPATH, "//*[@id='heading']/header/h2/span/a"
            ):
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

            if (
                len(driver.find_elements(By.XPATH, '//*[@id="show-hidden-efforts"]'))
                != 0
            ):
                while len(segment_tables) != 2:
                    try:
                        segment_tables = self._clicker(driver, 20)
                    except TimeoutException:

                        print(
                            "Timeout while waiting for the page to load. Reloading..."
                        )
                        driver.refresh()  # Refresh the page
                        segment_tables = self._clicker(driver, 20)
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
                for m, segment in enumerate(
                    segment_table.find_elements(By.TAG_NAME, "tr")
                ):
                    if m == 0 and g == 0:
                        pass
                    else:
                        segment_no.append(
                            segment.get_attribute("data-segment-effort-id")
                        )
                    for i, field in enumerate(segment.find_elements(By.TAG_NAME, "td")):
                        if i == 3:
                            segment_name.append(field.text.split("\n")[0])
                            segment_distance.append(
                                field.text.split("\n")[1].split(" ")[0]
                            )
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
            activity_dict_list["activities"].append(activity_dict)

            try:
                stats = driver.find_element(
                    By.XPATH, '//*[@id="heading"]/div/div/div[2]'
                )
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
                f"segment_{thread_id}_{self.year}_{self.grand_tour}.json",
                "w",
            ) as f:
                f.write(json_string)
            json_string = json.dumps(stat_dict_list)
            with open(
                f"stat_{thread_id}_{self.year}_{self.grand_tour}.json",
                "w",
            ) as f:
                f.write(json_string)
            time.sleep(3)

        driver.quit()
        return "All of the list scraped."
