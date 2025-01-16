import concurrent.futures
import pathlib
import pickle
import time
from pathlib import Path

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from grand_tours import chrome_grid_driver, getters


class ProCycling:

    def __init__(self, grand_tour, year_whole_list, logger, pro_path) -> None:

        self.logger = logger
        self.grand_tour = grand_tour
        self.max_workers = 3
        self.year_whole_list = year_whole_list
        self.pro_path = pro_path
        self.year_whole_list = self._split_into_n(
            self.year_whole_list, self.max_workers
        )
        print(self.year_whole_list)

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

    def _main_list_getter(self, year_list):
        driver = chrome_grid_driver.start_driver()
        main_list_pickle = []
        for year in year_list:
            stage_list = self._stage_getter(year, driver)
            for stage in stage_list:
                driver.get(
                    f"https://www.procyclingstats.com/race/{self.grand_tour}/"
                    + year
                    + "/stage-"
                    + stage.split(" ")[1]
                )
                time.sleep(3)

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
                                main_list = []
                main_list_pickle.append(
                    [
                        [int(year)] * len(main_list[0]),
                        [stage] * len(main_list[0]),
                        main_list,
                    ]
                )
            try:
                if (self.pro_path / f"main_{year_list[0]}_{int(year)+1}.pkl").exists():
                    pathlib.Path.unlink(
                        self.pro_path / f"main_{year_list[0]}_{int(year)+1}.pkl"
                    )

                with open(
                    self.pro_path / f"main_{year_list[0]}_{year}.pkl", "wb"
                ) as fp:  # Pickling
                    pickle.dump(main_list_pickle, fp)
            finally:
                driver.quit()

    def pro_scraper(self):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            (executor.map(self._main_list_getter, self.year_whole_list))
