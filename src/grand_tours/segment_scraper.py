import concurrent.futures
import gzip
import pickle
import threading
import time

import numpy as np
import undetected_chromedriver as uc
from rich import print
from rich import print as rprint
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SegmentScrape:
    def __init__(self, username, grand_tour: str, year: int, activity_whole_list, max_workers) -> None:
        self.username = username
        self.grand_tour = grand_tour
        self.year = year
        self.max_workers = max_workers
        self.activity_whole_list = activity_whole_list
        print(len(activity_whole_list))
        self.activity_whole_list = self._split_into_n(self.activity_whole_list, self.max_workers)

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
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        tables = driver.find_elements(By.CSS_SELECTOR, ".dense.hoverable.marginless.segments")
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dense.hidden-segments.hoverable.marginless"))
        )
        tables.append(driver.find_element(By.CSS_SELECTOR, ".dense.hidden-segments.hoverable.marginless"))

        return tables

    def _load_page_with_retry(self, driver, url, max_retries=5):
        retries = 0
        while retries < max_retries:
            try:
                rprint(f"[bold yellow] Attempt {retries + 1}: Trying to load URL: {url}[/bold yellow]")
                driver.execute_script("Object.defineProperty(navigator, 'webdrier', {get: () => undefined})")
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
            rprint("[bold red] Max retries reached. Could not load the page. [/bold red]")

    def segment_scraper(self):
        print(self.activity_whole_list)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for i, j in enumerate(self.activity_whole_list):
                # Submit each task with a slight delay
                futures[executor.submit(self._activity_data_getter, i + 1, j)] = j
                time.sleep(10)  # Adjust the sleep time as needed

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    rprint(f"[turquoise2] Task result:{result} [/turquoise2]")
                except Exception as e:
                    task_id = futures[future]
                    rprint(f"[bright red] Task {task_id} generated an exception: {e} [/bright red]")

    def _activity_data_getter(self, account_no, activity_no_list):
        print(f"for the account no {account_no} we have the table {activity_no_list}")
        thread_id = threading.get_ident()
        activity_main_list = []

        # setting profile
        # options.add_experimental_option("detach", "true")
        driver = uc.Chrome(
            user_data_dir=f"user-data-dir=/Users/deniz/Library/Application Support/Google/Chrome/Profile {account_no}",
            use_subprocess=True,
            version_main=133,
        )
        print("activated driver")

        for p, activity_no in enumerate(activity_no_list):
            activity_big_list = []
            activity = "https://www.strava.com/activities/" + str(activity_no)
            driver.get(activity)
            time.sleep(np.abs(np.random.randn()))

            # Extract the activity_type from the lightboxData JavaScript object
            # Find the script element containing pageProps
            script_element = driver.find_element(By.XPATH, "//script[contains(text(), 'pageProps')]")

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
                activity_main_list.append(activity_big_list)
                with gzip.open(
                    f"/Users/{self.username}/iCloud/Research/Data_Science/Projects/data/strava/{self.grand_tour}_pickles/segment_{thread_id}_{self.year}_{self.grand_tour}.pkl.gz",
                    "wb",
                ) as fp:  # Pickling
                    pickle.dump(activity_main_list, fp)

                time.sleep(3)
                continue

            # Get the summary container if it exists
            try:
                summary_container = driver.find_element(By.CSS_SELECTOR, ".row.no-margins.activity-summary-container")
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
                        segment_tables = self._clicker(driver, 20)
                        segment_tables = [i.get_attribute("innerHTML") for i in segment_tables]
                    except TimeoutException:
                        print("Timeout while waiting for the page to load. Reloading...")
                        driver.refresh()  # Refresh the page
                        segment_tables = self._clicker(driver, 20)
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
                segment_tables = driver.find_elements(By.CSS_SELECTOR, ".dense.hoverable.marginless.segments")
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
            with gzip.open(
                f"/Users/{self.username}/iCloud/Research/Data_Science/Projects/data/strava/{self.grand_tour}_pickles/segment_{thread_id}_{self.year}_{self.grand_tour}.pkl.gz",
                "wb",
            ) as fp:  # Pickling
                pickle.dump(activity_main_list, fp)

            time.sleep(4)

        driver.quit()
        return "All of the list scraped."


def anal_scrape(driver, activity_no, stage):
    dict_list = []
    activity = "https://www.strava.com/activities/" + str(activity_no) + "/analysis "
    driver.get(activity)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="segmentBars"]')
        )  # Replace with a specific element for better accuracy
    )
    # This one allows the hovering over elements
    actions = ActionChains(driver)

    segments_chart = driver.find_element(By.XPATH, '//*[@id="segments-chart"]')
    segments_box = driver.find_element(By.XPATH, '//*[@id="segmentBars"]')

    segments = segments_box.find_elements(By.TAG_NAME, "rect")

    for rect_element in segments:
        # Hover over the element
        actions.move_to_element(rect_element).perform()
        time.sleep(5)
        # Get attributes
        x = rect_element.get_attribute("x")
        y = rect_element.get_attribute("y")
        width = rect_element.get_attribute("width")
        segment_name = segments_chart.text.split("\n")[0]
        extras = segments_chart.text.split("\n")[1]

        # Print the attributes
        attributes = {
            "activity_id": activity_no,
            "stage": stage,
            "segment_name ": segment_name,
            "x ": x,
            "y": y,
            "width": width,
            "extras": extras,
        }
        print(attributes)
        dict_list.append(attributes)

    return dict_list
