import os
import time

import undetected_chromedriver as uc
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def _strava_login(email, password):

    print(email)
    driver = uc.Chrome()
    # open strava
    driver.get("https://www.strava.com")

    # Give the browser time to load all content.
    time.sleep(2)

    # click login button
    driver.find_element(
        By.XPATH, '//*[@id="__next"]/div[2]/div[1]/nav/div/div[1]/div[2]/button'
    ).click()

    time.sleep(3)

    # click don't remember me
    driver.find_element(
        By.XPATH,
        '//*[@id="__next"]/div/div[2]/div[2]/div/div[2]/form/div[3]/label',
    ).click()
    time.sleep(1)

    # enter email
    driver.find_element(By.XPATH, '//*[@id="desktop-email"]').send_keys(f"{email}")

    # click first login for email
    driver.find_element(By.XPATH, '//*[@id="desktop-login-button"]').click()
    time.sleep(3)

    # enter password
    driver.find_element(
        By.XPATH,
        '//*[@id="__next"]/div/div[2]/div[2]/div/div/form/div[1]/div[2]/div/input',
    ).send_keys(f"{password}")

    time.sleep(2)

    driver.find_element(
        By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div/div/form/div[2]/button'
    ).click()

    time.sleep(10)

    driver.quit()


if __name__ == "__main__":

    load_dotenv()
    _strava_login(os.getenv("STRAVA_EMAIL_1"), os.getenv("STRAVA_PASSWORD_1"))
