import getpass

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def driver_single():
    service = Service()
    options = Options()
    username = getpass.getuser()
    options.add_experimental_option("detach", True)
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-proxy-server")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--blink-settings=imagesEnabled=false")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_argument(
    #    "user-data-dir=/Users/dmini/Library/Application Support/Google/Chrome/Profile 1"
    # )
    options.add_argument(
        f"--user-data-dir=/Users/{username}/Library/Application Support/Google/Chrome/"
    )
    options.add_argument(f"--profile-directory=Profile 1")
    return webdriver.Chrome(service=service, options=options)
