from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Remote(command_executor="http: //www.example.com")
options = chrome_options
driver.get("http://www.google.com")
driver.quit()
