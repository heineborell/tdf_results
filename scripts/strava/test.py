import os
import time

import undetected_chromedriver as uc
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _strava_login(email, password):

    print(email)
    print(password)
    options = uc.ChromeOptions()
    # options.add_argument(
    #    f"--user-data-dir=/Users/{username}/Library/Application Support/Google/Chrome/"
    # )
    # options.add_argument(f"--profile-directory=Profile 2")
    # setting profile
    # options.user_data_dir = (
    #    "/Users/deniz/Library/Application Support/Google/Chrome/Profile 1"
    # )
    driver = uc.Chrome()
    driver.delete_all_cookies()
    # open strava
    driver.get("https://www.strava.com")

    # Give the browser time to load all content.
    time.sleep(5)

    # click login button
    driver.find_element(
        By.XPATH, '//*[@id="__next"]/div[2]/div[1]/nav/div/div[1]/div[2]/button'
    ).click()

    time.sleep(5)

    # click cookies button
    # driver.find_element(
    #    By.XPATH, ' //*[@id="__next"]/div[1]/div/div/button[1] '
    # ).click()

    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="__next"]/div[2]/div[1]/nav/div/div[1]/div[2]/button',
                    )
                )
            )
            # click don't remember me
            driver.find_element(
                By.XPATH,
                '//*[@id="__next"]/div/div[2]/div[2]/div/div[2]/form/div[3]/label',
            ).click()
            time.sleep(5)

            # enter email
            driver.find_element(By.XPATH, '//*[@id="desktop-email"]').send_keys(
                f"{email}"
            )

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="desktop-login-button"]')
                )
            )
            # click first login for email
            driver.find_element(By.XPATH, '//*[@id="desktop-login-button"]').click()
            time.sleep(5)

            # enter password
            driver.find_element(
                By.XPATH,
                '//*[@id="__next"]/div/div[2]/div[2]/div/div/form/div[1]/div[2]/div/input',
            ).send_keys(f"{password}")

            time.sleep(5)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="__next"]/div/div[2]/div[2]/div/div/form/div[2]/button',
                    )
                )
            )
            driver.find_element(
                By.XPATH,
                '//*[@id="__next"]/div/div[2]/div[2]/div/div/form/div[2]/button',
            ).click()

            time.sleep(10)
            # Perform actions when the element is found
        except (NoSuchElementException, TimeoutException):
            print("Element not found within the timeout period")
            break

    driver.quit()


if __name__ == "__main__":

    load_dotenv()
    _strava_login(os.getenv("STRAVA_EMAIL_2"), os.getenv("STRAVA_PASSWORD_2"))
