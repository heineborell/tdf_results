from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth


def chrome_stealth():
    # ChromeDriver path
    CHROMEDRIVER_PATH = "/opt/chromedriver/chromedriver-linux64/chromedriver"  # Adjust to your actual path
    CHROME_BINARY_PATH = "/opt/chrome/chrome-linux64/chrome"
    # /opt/chrome/chrome-linux64

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.binary_location = CHROME_BINARY_PATH
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless=new")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Set up ChromeDriver with explicit path
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Apply stealth settings
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Linux x86_64",  # Correct platform for Intel machines on Debian
        webgl_vendor="Intel Open Source Technology Center",
        renderer="Mesa Intel(R) UHD Graphics 620 (Kabylake GT2)",
        fix_hairline=True,
    )

    return driver
