import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--headless=new")  # Enable headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Set up ChromeDriver
service = Service(ChromeDriverManager().install())
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

# Test the stealth setup
driver.get("https://www.strava.com")

# Give the browser time to load all content.
time.sleep(5)

# click login button
driver.find_element(
    By.XPATH, '//*[@id="__next"]/div[2]/div[1]/nav/div/div[1]/div[2]/button'
).click()

time.sleep(5)
print(driver.page_source)

# Close the browser
driver.quit()
