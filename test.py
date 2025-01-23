import undetected_chromedriver as uc

driver = uc.Chrome(
    driver_executable_path="/opt/chromedriver/chromedriver-linux64/chromedriver",
    browser_executable_path="/opt/chrome/chrome-linux64/chrome",
    headless=True,
)
driver.get("https://www.strava.com")
driver.quit()
