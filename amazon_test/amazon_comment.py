from pipeline import MySQLPipline
import time
from playwright.sync_api import Playwright, sync_playwright, expect
asin_list = ["B07PBFNYXV","B0B8ZD47L8","B0074UZV2G","B06ZYNZ7NF","B074H73B2K","B00GSL2RRO","B074H5SR5S","B00G0JHHNS","B00UJAJ2IM","B00PGXQ68Q","B0BWBP3T8B","B07FW6T2PW","B00LEXYEK4",
            "B000LKZ3GA","B00GSL34KI","B00VTR0UFI","B07NW4GSSR","B09DMV2XFX"]
mysql = MySQLPipline()
redis_key = 'amazon_comment'
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
        get_data(page, asin,'')
    context.close()
    browser.close()

def get_data(page,asin ,url):
    if not url:
        url = f'https://www.amazon.com/product-reviews/{asin}'
    try:
        page.goto(url)  #["commit", "domcontentloaded", "load", "networkidle"]
        comment_list =  page.query_selector_all('//*[@id="cm_cr-review_list"]/div')
        for comment in comment_list:
            data = {}
            data['asin_id'] = asin
            data['comment_url'] = url
            data['comment_avatar'] = get_xpath(comment,'//*[@class="a-profile-avatar"]/img','src') #用户头像
            data['comment_username'] = get_xpath(comment,'//*[@class="a-profile-name"]',text=True) #用户昵称
            data['comment_star_score'] = get_xpath(comment,'//*[@class="a-icon-alt"]',text=True) #用户评分
            data['comment_topic'] = get_xpath(comment,'//*[@data-hook="review-title"]/span',text = True) #评论标题
            data['comment_reviewed_time_loc'] = get_xpath(comment,'//*[@data-hook="review-date"]',text=True)  #评论时间地点
            data['comment_product_info'] = get_xpath(comment,'//*[@data-hook="format-strip"]',text=True)  #产品信息
            data['comment_body'] = get_xpath(comment,'//*[@data-hook="review-body"]/span',text=True)  # 评论内容
            data['comment_helpful'] = get_xpath(comment,'//*[@data-hook="helpful-vote-statement"]',text=True)  # n人认为有帮助的
            data['comment_image'] = get_xpath(comment,'//*[@data-hook="review-image-tile"]','src') #评论图片
            if data['comment_avatar']:mysql.submit_item(data, redis_key) #有时候会出现没有数据的情况，所以要用头像进行校验，头像是必有的
        next_page = get_xpath(page, 'text=Next page', 'href', is_text=True)  # 获取下一页的链接，没有说明没有下一页
        if next_page:
            # asin_id = next_page.split('product-reviews/',1)[1].split('/ref=',1)[0]
            get_data(page,asin,url = f'https://www.amazon.com{next_page}')
    except Exception as e:
        print(f'评论获取出错啦{url}---{e}')



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
