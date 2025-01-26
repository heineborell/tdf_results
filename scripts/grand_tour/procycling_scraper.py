from pathlib import Path

import pandas as pd
from selenium.webdriver.common.by import By

from grand_tours import chrome_driver, getters, logger_config, proscraper

# GRAND_TOUR = "tour-de-france"
# GRAND_TOUR = "giro-d-italia"
GRAND_TOUR = "vuelta-a-espana"

if GRAND_TOUR == "tour-de-france":
    pro_path = Path.cwd().parent.parent / "data/pro_tdf/"
elif GRAND_TOUR == "giro-d-italia":
    pro_path = Path.cwd().parent.parent / "data/pro_giro/"
elif GRAND_TOUR == "vuelta-a-espana":
    pro_path = Path.cwd().parent.parent / "data/pro_vuelta/"


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
logger = logger_config.setup_logger("app.log")

# Local driver just for year list
driver_year = chrome_driver.start_driver()
driver_year.get(f"https://www.procyclingstats.com/race/{GRAND_TOUR}/2024/stage-11")
info_dict = getters.get_info_dict(driver_year)
info_df = pd.DataFrame(columns=list(info_dict.keys()))
drop_list = driver_year.find_elements(By.CLASS_NAME, "pageSelectNav ")
year_element = drop_list[0].find_elements(By.TAG_NAME, "option")
year_list = [year.text for year in year_element]
driver_year.quit()

print(year_list)

del year_list[0]

scraper = proscraper.ProCycling(GRAND_TOUR, year_list, logger, 10, pro_path)
scraper.pro_scraper()
