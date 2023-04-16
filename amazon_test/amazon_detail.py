from pipeline import MySQLPipline
import time
from playwright.sync_api import Playwright, sync_playwright, expect
import os
import threading
asin_list = ["B07PBFNYXV","B0B8ZD47L8","B0074UZV2G","B06ZYNZ7NF","B074H73B2K","B00GSL2RRO","B074H5SR5S","B00G0JHHNS","B00UJAJ2IM","B00PGXQ68Q","B0BWBP3T8B","B07FW6T2PW","B00LEXYEK4",
            "B000LKZ3GA","B00GSL34KI","B00VTR0UFI","B07NW4GSSR","B09DMV2XFX"]
mysql = MySQLPipline()
redis_key = 'amazon_detail'
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
    time.sleep(2)
    for asin in asin_list:
        get_data(page, asin)
    context.close()
    browser.close()

def get_data(page,asin):
    url = f'https://www.amazon.com/dp/{asin}/ref=sr_1_1_sspa'
    page.goto(url,wait_until = 'domcontentloaded')  #["commit", "domcontentloaded", "load", "networkidle"]
    data = {}
    data['asin_id'] = asin
    data['image'] = get_xpath(page, "//*[contains(@class,'imgTagWrapper')]/img", 'src')  # 主图
    data['ratings'] = get_xpath(page, '//*[@id="acrCustomerReviewText"]', text=True)  # 评论数
    data['answered_questions'] = get_xpath(page, '//*[@id="askATFLink"]/span', text=True)  # qa数量
    data['brand'] = get_xpath(page, '//*[@id="bylineInfo"]', text=True)  # 商标
    data['star_avg'] = get_xpath(page,'//*[@id="reviewsMedley"]//div[@class="a-row"]/span[@class="a-size-base a-nowrap"]/span[@data-hook="rating-out-of-text"]',text=True)  # 星评
    data['comment_url'] = get_xpath(page, '//*[@id="reviews-medley-footer"]/div[2]/a', 'href')
    data['qa_url'] = f'https://www.amazon.com/ask/questions/asin/{asin}'
        # get_xpath(page,"a:text-matches('See more answered questions.*')",'href',is_text=True)  #需要全局加载才行

    print(url,f'pageid是{id(page)}当前进程id{threading.current_thread().ident},线程id是{os.getppid()}')
    mysql.submit_item(data, redis_key)
    # if data['comment_url'] : amazon_comment.get_data(data['comment_url'])  #去获取评论数据



def get_xpath(page,xpath,attribute = '',text = False,is_text = False):
    '''默认是通过xpath获取属性的 text为true获取文本  is_test为True是通过文本查找selector
    :param page: 浏览器对象
    :param xpath: 定位selector的xpath
    :param attribute: 获取的属性key
    :param text: 是否获取文本
    :param is_text: 是否通过文本定位selector
    :return:
    '''
    if attribute:
        if page.query_selector(xpath):
            if page.query_selector(xpath).get_attribute(attribute):
                a = data_clean(page.query_selector(xpath).get_attribute(attribute))
                return a
    elif text:
        if page.query_selector(xpath):
            if page.query_selector(xpath).text_content():
                a = data_clean(page.query_selector(xpath).text_content())
                return a
    return ''


def data_clean(str):
    #数据清洗
    str = str.replace('\n','',).strip().replace('"',"'").replace('\\','\\\\')
    return str



with sync_playwright() as playwright:
    run(playwright)
