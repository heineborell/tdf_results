import json

from selenium.webdriver.support.ui import WebDriverWait

from grand_tours import chrome_driver, segment_details

if __name__ == "__main__":
    driver = chrome_driver.start_driver(
        detach=False, additional_options={"headless": True}
    )
    wait = WebDriverWait(driver, 5)

    activity_no = 12957753457
    dict_list = segment_details.segment_details_scrape(activity_no, driver)

    json_string = json.dumps(dict_list)
    with open(
        f"segments.json",
        "w",
    ) as f:
        f.write(json_string)
