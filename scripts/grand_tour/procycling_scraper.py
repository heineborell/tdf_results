import pathlib
import time
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from grand_tours import chrome_driver, getters, logger_config

# GRAND_TOUR = "tour-de-france"
GRAND_TOUR = "giro-d-italia"
if GRAND_TOUR == "tour-de-france":
    pro_path = Path.cwd().parent.parent / "data/pro_tdf/"
elif GRAND_TOUR == "giro-d-italia":
    pro_path = Path.cwd().parent.parent / "data/pro_giro/"


if pro_path.exists():
    print("Folder pro_path exists.")
else:
    pro_path.mkdir()
    print("Folder pro_path created.")

if (pro_path / "info").exists():
    print("Folder pro_path/info exists.")
else:
    (pro_path / "info").mkdir()
    print("Folder pro_path/info created.")

# Logger
logger = logger_config.setup_logger()

# Driver
driver = chrome_driver.start_driver(detach=False, additional_options={"headless": True})

driver.get(f"https://www.procyclingstats.com/race/{GRAND_TOUR}/2024/stage-11")
df = pd.DataFrame(columns=["year", "stage", "name", "time"])


info_dict = getters.get_info_dict(driver)

info_df = pd.DataFrame(columns=list(info_dict.keys()))

drop_list = driver.find_elements(By.CLASS_NAME, "pageSelectNav ")
year_element = drop_list[0].find_elements(By.TAG_NAME, "option")
year_list = [year.text for year in year_element]

# use this to choose what year you want to scrape
# year_list = year_list[23:]
del year_list[0]

for year in year_list:
    logger.info(f"------{year}------")
    driver.get(f"https://www.procyclingstats.com/race/{GRAND_TOUR}/" + year + "/")
    drop_list = driver.find_elements(By.CLASS_NAME, "pageSelectNav ")
    time.sleep(2)
    if len(drop_list) == 2:
        stage_element = drop_list[1].find_elements(By.TAG_NAME, "option")
        stage_list = [stage.text for stage in stage_element if "Stage" in stage.text]
    elif len(drop_list) == 3:
        stage_element = drop_list[2].find_elements(By.TAG_NAME, "option")
        stage_list = [stage.text for stage in stage_element if "Stage" in stage.text]

    for i, stage in enumerate(stage_list):
        logger.info(f"----{stage}")
        driver.get(
            f"https://www.procyclingstats.com/race/{GRAND_TOUR}/"
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
                    ttt_val = 0
                    main_list = getters.get_tables(driver, ".results.basic.moblist12")
                    logger.info("It is a normal stage.")

        if (
            ttt_val == 0
            and not set(main_list[1]) == {",,"}
            and not set(main_list[1]) == {""}
        ):

            for j, _ in enumerate(main_list[1]):

                if main_list[1][j] != ",," and "-" not in main_list[1][j]:
                    try:
                        # The following exceptions area for time formats ans their parsing
                        t = datetime.strptime(main_list[1][j], "%H:%M:%S")
                        main_list[1][j] = int(
                            timedelta(
                                hours=t.hour, minutes=t.minute, seconds=t.second
                            ).total_seconds()
                        )

                    except ValueError:
                        # This final exception is for the results that don't fit any time format
                        try:
                            if "," not in main_list[1][j]:
                                t = datetime.strptime(main_list[1][j], "%M:%S")
                                main_list[1][j] = int(
                                    timedelta(
                                        hours=t.hour, minutes=t.minute, seconds=t.second
                                    ).total_seconds()
                                )
                            else:
                                stripped_t = main_list[1][j][
                                    0 : main_list[1][j].index(",")
                                ]
                                t = datetime.strptime(stripped_t, "%M.%S")
                                main_list[1][j] = int(
                                    timedelta(
                                        hours=t.hour, minutes=t.minute, seconds=t.second
                                    ).total_seconds()
                                )
                        except ValueError:
                            logger.error("No time format fits!")
                            break
            # this part is for dealing with '' and time increments
            for j, _ in enumerate(main_list[1]):
                if isinstance(main_list[1][j], int) and j > 0:
                    main_list[1][j] = main_list[1][j] + main_list[1][0]

            for j, _ in enumerate(main_list[1]):
                if main_list[1][j] == ",,":
                    main_list[1][j] = main_list[1][j - 1]

            info_lst = [info.text for info in main_list[2]]
            final_info_lst = []
            for i in info_lst:
                if len(i.split("\n")) == 1:
                    single_el = i.split("\n")
                    single_el.append("Na")
                    final_info_lst.append(single_el)
                else:
                    final_info_lst.append(i.split("\n"))

            final_info_lst = np.array(final_info_lst).flatten()

            # construct info table dictionary
            info_dict = dict(zip(final_info_lst[0::2], final_info_lst[1::2]))
            info_dict = {
                k: [v] for k, v in info_dict.items()
            }  # this is needed as pandas want an index (kinda hack solution)
            info_df = pd.concat(
                [info_df, pd.DataFrame.from_dict(info_dict)], ignore_index=True
            )
            final_dict = {
                "year": [int(year)] * len(main_list[0]),
                "stage": [stage] * len(main_list[0]),
                "name": main_list[0],
                "time": main_list[1],
            }
            info_dict_ext = {k: v * len(main_list[0]) for k, v in info_dict.items()}
            final_dict = final_dict | info_dict_ext

            df = pd.concat(
                [
                    df,
                    pd.DataFrame(final_dict),
                ]
            )
            if (pro_path / f"pro_{year_list[0]}_{int(year)+1}.csv").exists():
                pathlib.Path.unlink(pro_path / f"pro_{year_list[0]}_{int(year)+1}.csv")

            if (
                pro_path / "info" / f"infodf_{year_list[0]}_{int(year)+1}.csv"
            ).exists():
                pathlib.Path.unlink(
                    pro_path / "info" / f"infodf_{year_list[0]}_{int(year)+1}.csv"
                )

            df.to_csv(pro_path / f"pro_{year_list[0]}_{year}.csv")
            info_df.to_csv(pro_path / "info" / f"infodf_{year_list[0]}_{year}.csv")

        else:
            # This is the TTT exception we made way above
            logger.info(
                "If its normal the entries are empty if its not it is a TTT stage"
            )

driver.quit()
