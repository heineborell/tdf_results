import concurrent.futures

from selectolax.parser import HTMLParser
from selenium import webdriver

urls = [
    "https://www.amazon.co.uk/dp/B0002E4Z8M",
    "https://www.amazon.co.uk/dp/B004MQSV04",
    "https://www.amazon.co.uk/dp/B002YUAK54",
    "https://www.amazon.co.uk/dp/B0006H92QK",
    "https://www.amazon.co.uk/dp/B00M9CUOKI",
    "https://www.amazon.co.uk/dp/B07QR6Z1JB",
    "https://www.amazon.co.uk/dp/B08Q1NJSBQ",
    "https://www.amazon.co.uk/dp/B07MSCRCVK",
]


def get_html(url):
    options = webdriver.ChromeOptions()
    grid_url: str = "http://localhost:4444"
    driver = webdriver.Remote(command_executor=grid_url, options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html


def parse_html(html):
    data = HTMLParser(html)
    return {
        "title": data.css_first("title").text(strip=True),
        "price": data.css_first("span.a-offscreen").text(strip=True),
    }


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(get_html, urls))


for res in results:
    print(parse_html(res))
