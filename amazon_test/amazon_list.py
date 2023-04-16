import time

from playwright.sync_api import Playwright, sync_playwright, expect
from lxml import etree
from pipeline import MySQLPipline
keyword_list = ['milk']
current_page_number = 0
mysql = MySQLPipline()
redis_key = 'amazon_list'
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(geolocation={"latitude": 34.1227, "longitude": 118.7573}, locale="en-UA",
                                  permissions=["geolocation"], timezone_id="America/Los_Angeles")
    page = context.new_page()
    page.goto("https://www.amazon.com/",wait_until = "load")
    page.get_by_role("button", name="Submit").nth(1).click()
    page.get_by_role("textbox", name="or enter a US zip code").click()
    page.get_by_role("textbox", name="or enter a US zip code").fill("91301")
    time.sleep(0.3)
    page.locator("#GLUXZipUpdate").get_by_role("button", name="Apply").click(no_wait_after = True)
    page.get_by_role("button", name="Continue").click()
    time.sleep(1)

    for kw in keyword_list:
        for i in range(2):
            url = f'https://www.amazon.com/s?k={kw}&page={i+1}'
            get_data(page,url)
    context.close()
    browser.close()

# def on_response(response):
#     if 'apparel' in response.url and response.status == 200:
#         print(response.json())

def get_data(page,url):
    page.goto(url)
    data = {}
    goods_list = page.query_selector_all('//*[@class="s-main-slot s-result-list s-search-results sg-row"]/div')
    for goods in goods_list:
        asin_id = goods.get_attribute('data-asin')
        rank = goods.get_attribute('data-index')
        data['asin_id'] = asin_id
        data['kw_rank'] = rank
        mysql.submit_item(data,redis_key)



with sync_playwright() as playwright:
    run(playwright)
