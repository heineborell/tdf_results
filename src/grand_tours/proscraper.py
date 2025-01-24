import concurrent.futures
import pathlib
import pickle
import threading
import time

from rich import print as rprint
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from grand_tours import chrome_grid_driver, getters


class ProCycling:

    def __init__(
        self, grand_tour, year_whole_list, logger, max_workers, pro_path
    ) -> None:

        self.logger = logger
        self.grand_tour = grand_tour
        self.max_workers = max_workers
        self.year_whole_list = year_whole_list
        self.pro_path = pro_path
        self.year_whole_list = self._split_into_n(
            self.year_whole_list, self.max_workers
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

    def _stage_getter(self, year, driver):

        driver.get(
            f"https://www.procyclingstats.com/race/{self.grand_tour}/" + year + "/"
        )
        drop_list = driver.find_elements(By.CLASS_NAME, "pageSelectNav ")
        time.sleep(2)
        if len(drop_list) == 2:
            stage_element = drop_list[1].find_elements(By.TAG_NAME, "option")
            stage_list = [
                stage.text for stage in stage_element if "Stage" in stage.text
            ]
        elif len(drop_list) == 3:
            stage_element = drop_list[2].find_elements(By.TAG_NAME, "option")
            stage_list = [
                stage.text for stage in stage_element if "Stage" in stage.text
            ]

        return stage_list

    def _load_page_with_retry(self, driver, year, stage, max_retries=5):
        retries = 0
        url = f"https://www.procyclingstats.com/race/{self.grand_tour}/{year}/stage-{stage.split(' ')[1]}"
        while retries < max_retries:
            try:
                rprint(
                    f"[bold yellow] Attempt {retries + 1}: Trying to load URL: {year}-stage-{stage} [/bold yellow]"
                )
                driver.get(url)

                # Wait for a specific element to confirm page load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, "body")
                    )  # Replace with a specific element for better accuracy
                )
                rprint("[bold green] Page loaded successfully! [/bold green]")
                break  # Exit the loop if the page loads successfully
            except TimeoutException:
                retries += 1
                rprint(
                    f"[bold red] Retry {retries}/{max_retries}: Page did not load completely. Retrying...[/bold red]"
                )
                time.sleep(3)  # Optional wait before retrying
        else:
            print("Max retries reached. Could not load the page.")

    def _main_list_getter(self, year_list):
        thread_id = threading.get_ident()
        driver = chrome_grid_driver.start_driver()
        main_list_pickle = []
        for year in year_list:
            stage_list = self._stage_getter(year, driver)
            for stage in stage_list:
                self._load_page_with_retry(driver, year, stage)

                # Throwing the stages with no moblist
                if (driver.page_source.find("moblist")) == -1:
                    self.logger.info(f"---{year}---{stage}---No moblist!")
                    continue

                try:
                    main_list = getters.get_tables(driver, ".results.basic.moblist11")

                except NoSuchElementException:

                    try:
                        # this exception for ttt stages which I just dropped out
                        driver.find_element(By.CLASS_NAME, "results-ttt")
                        main_list = getters.get_tables_ttt(driver, "results-ttt")
                        self.logger.info(f"---{year}---{stage}---Its a TTT stage!")
                    except NoSuchElementException:
                        try:
                            main_list = getters.get_tables(
                                driver, ".results.basic.moblist10"
                            )
                            self.logger.info(
                                f"---{year}---{stage}---Its a normal stage!"
                            )
                            if (
                                len(main_list[1]) == 0
                            ):  # this is basically to continue down to moblist12 if moblist10 empty
                                raise NoSuchElementException("Empty list.")
                        except NoSuchElementException:
                            try:
                                main_list = getters.get_tables(
                                    driver, ".results.basic.moblist12"
                                )
                                self.logger.info(
                                    f"---{year}---{stage}---Its a normal stage!"
                                )
                            except NoSuchElementException:
                                self.logger.info(f"---{year}---{stage}---No moblist!")
                                main_list = [[], [], []]
                main_list_pickle.append(
                    [
                        [int(year)] * len(main_list[0]),
                        [stage] * len(main_list[0]),
                        main_list,
                    ]
                )
                if (
                    self.pro_path / f"{thread_id}_{year_list[0]}_{int(year)+1}.pkl"
                ).exists():
                    pathlib.Path.unlink(
                        self.pro_path / f"{thread_id}_{year_list[0]}_{int(year)+1}.pkl"
                    )

                with open(
                    self.pro_path / f"{thread_id}_{year_list[0]}_{year}.pkl", "wb"
                ) as fp:  # Pickling
                    pickle.dump(main_list_pickle, fp)
        driver.quit()
        return "Finished ok!"

    def pro_scraper(self):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            futures = {
                executor.submit(self._main_list_getter, i): i
                for i in self.year_whole_list
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
