import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

driver = uc.Chrome(
    driver_executable_path="/opt/chromedriver/chromedriver-linux64/chromedriver",
    browser_executable_path="/opt/chrome/chrome-linux64/chrome",
    headless=True)

driver.get("https://www.strava.com/login")

 # Give the browser time to load all content.
time.sleep(2)

print(driver.page_source)
# Find element by tag
#element = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[1]/div[1]/div[2]')

# Print the text of the element
#strava_entry=driver.get("https://www.strava.com")
#print(strava_entry.get_attribute('innerHTML'))
driver.quit()
