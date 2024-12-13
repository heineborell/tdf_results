import getpass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def start_driver():
    """Initialize Chrome Driver with options"""
    service = Service()
    username = getpass.getuser()
    options = Options()
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(
        f"user-data-dir=/Users/{username}/Library/Application Support/Google/Chrome/Profile 1"
    )
    options.page_load_strategy = (
        "eager"  # Scraper doesn't wait for browser to load all the page
    )

    return webdriver.Chrome(service=service, options=options)
