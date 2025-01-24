import os
import time

import undetected_chromedriver as uc
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.delete_all_cookies()
# open strava
driver.get("https://bot.sannysoft.com/")
time.sleep(20)
driver.quit()
