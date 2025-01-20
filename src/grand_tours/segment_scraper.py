import json
import time

import numpy as np
import pandas as pd
from rich import print as rprint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine

import grand_tours
from grand_tours import chrome_driver, chrome_grid_driver


class SegmentScrape:
    def __init__(self, grand_tour, year) -> None:
        self.grand_tour = grand_tour
        self.year = year

    def _load_page_with_retry(self, driver, url, max_retries=5):
        retries = 0
        while retries < max_retries:
            try:
                rprint(
                    f"[bold yellow] Attempt {retries + 1}: Trying to load URL: {url}[/bold yellow]"
                )
                driver.execute_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
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
            rprint(
                "[bold red] Max retries reached. Could not load the page. [/bold red]"
            )

    def _login_strava(self, driver, email, password):
        # Locate the email input field
        email_input = driver.find_element(By.XPATH, '//*[@id="desktop-email"]')
        password_input = driver.find_element(
            By.XPATH, '//*[@id="desktop-current-password"]'
        )

        # Enter the email
        email_input.send_keys(email)
        time.sleep(5)
        # Enter the pass
        password_input.send_keys(password)
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="desktop-login-button"]').click()

    def scrape(self):
        url = "https://www.strava.com"
        driver = chrome_grid_driver.start_driver()
        self._load_page_with_retry(driver, url)
        print(
            driver.find_element(
                By.XPATH, '//*[@id="athlete-profile"]/div[1]/a/h2/div'
            ).text
        )
        # self._login_strava(driver, "pederramirez@gmail.com", "zabNor-6cawra-hyxtiv")
