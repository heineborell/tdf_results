import pathlib
import pickle
import time
from pathlib import Path

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from grand_tours import getters


def stage_getter(year, grand_tour, driver, logger):
    logger.info(f"------{year}------")
    driver.get(f"https://www.procyclingstats.com/race/{grand_tour}/" + year + "/")
    drop_list = driver.find_elements(By.CLASS_NAME, "pageSelectNav ")
    time.sleep(2)
    if len(drop_list) == 2:
        stage_element = drop_list[1].find_elements(By.TAG_NAME, "option")
        stage_list = [stage.text for stage in stage_element if "Stage" in stage.text]
    elif len(drop_list) == 3:
        stage_element = drop_list[2].find_elements(By.TAG_NAME, "option")
        stage_list = [stage.text for stage in stage_element if "Stage" in stage.text]

    return stage_list


def main_list_getter(year, grand_tour, stage_list, driver, logger, pro_path):
    main_list_pickle = {}
    year_list = []
    year_list.append(year)
    for stage in stage_list:
        logger.info(f"----{stage}")
        driver.get(
            f"https://www.procyclingstats.com/race/{grand_tour}/"
            + year
            + "/stage-"
            + stage.split(" ")[1]
        )
        time.sleep(3)

        # Throwing the stages with no moblist
        if (driver.page_source.find("moblist")) == -1:
            logger.info("No moblist!")
            continue

        try:
            main_list = getters.get_tables(driver, ".results.basic.moblist11")

            ttt_val = 0
        except NoSuchElementException:

            try:
                # this exception for ttt stages which I just dropped out
                ttt_test = driver.find_element(By.CLASS_NAME, "results-ttt")
                ttt_val = 1
            except NoSuchElementException:
                try:
                    ttt_val = 0
                    main_list = getters.get_tables(driver, ".results.basic.moblist10")
                    logger.info("It is a normal stage.")
                    if (
                        len(main_list[1]) == 0
                    ):  # this is basically to continue down to moblist12 if moblist10 empty
                        raise NoSuchElementException("Empty list.")
                except NoSuchElementException:
                    try:
                        ttt_val = 0
                        main_list = getters.get_tables(
                            driver, ".results.basic.moblist12"
                        )
                        logger.info("It is a normal stage.")
                    except NoSuchElementException:
                        logger.info("No moblist!")

        main_list[2] = [info.text for info in main_list[2]]
        main_list_pickle.update({f"{year}": main_list})
        if (pro_path / f"main_{year_list[0]}_{int(year)+1}").exists():
            pathlib.Path.unlink(pro_path / f"pro_{year_list[0]}_{int(year)+1}")

        with open(pro_path / f"main_{year_list[0]}_{year}", "wb") as fp:  # Pickling
            pickle.dump(main_list_pickle, fp)
