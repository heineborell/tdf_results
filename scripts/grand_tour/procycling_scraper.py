from pathlib import Path

import pandas as pd
from selenium.webdriver.common.by import By

from grand_tours import chrome_driver, getters, logger_config, proscraper

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

# [['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014'], ['2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003'], ['2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992'], ['1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983', '1982', '1981'], ['1980', '1979', '1978', '1977', '1976', '1975', '1974', '1973', '1972', '1971', '1970'], ['1969', '1968', '1967', '1966', '1965', '1964', '1963', '1962', '1961', '1960', '1959'], ['1958', '1957', '1956', '1955', '1954', '1953', '1952', '1951', '1950', '1949', '1948'], ['1947', '1946', '1940', '1939', '1938', '1937', '1936', '1935', '1934', '1933'], ['1932', '1931', '1930', '1929', '1928', '1927', '1926', '1925', '1924', '1923'], ['1922', '1921', '1920', '1919', '1914', '1913', '1912', '1911', '1910', '1909']]
