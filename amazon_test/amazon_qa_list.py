import threading

from pipeline import MySQLPipline
import time
import traceback

from playwright.sync_api import Playwright, sync_playwright, expect
asin_list = ["B07PBFNYXV","B0B8ZD47L8","B0074UZV2G","B06ZYNZ7NF","B074H73B2K","B00GSL2RRO","B074H5SR5S","B00G0JHHNS","B00UJAJ2IM","B00PGXQ68Q","B0BWBP3T8B","B07FW6T2PW","B00LEXYEK4",
            "B000LKZ3GA","B00GSL34KI","B00VTR0UFI","B07NW4GSSR","B09DMV2XFX"]
mysql = MySQLPipline()
redis_key = 'amazon_qa'
redis_detail_key = 'amazon_qa_detail'
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

def get_data(page,asin,url):
    if not url:
        url = f'https://www.amazon.com/ask/questions/asin/{asin}'
    try:
        detail_list = []
        page.goto(url)  #["commit", "domcontentloaded", "load", "networkidle"]
        qa_list =  page.query_selector_all('//*[@class="a-section askTeaserQuestions"]/div')
        next_page = get_xpath(page, 'text=Next', 'href', is_text=True)  # 获取下一页的链接，没有说明没有下一页
        for qa in qa_list:
            data = {}
            data['asin_id'] = asin
            data['qa_url'] = url
            data['qa_question'] = get_xpath(qa,'//*/div[@class="a-fixed-left-grid-col a-col-right"]/a/span[@class="a-declarative"]',text=True) #问题
            shot_text = get_xpath(qa, '//*/div[@class="a-fixed-left-grid-col a-col-right"]/span', text=True)  # 详细回答
            if shot_text:
                data['qa_answer'] = shot_text
            else:
                data['qa_answer'] = get_xpath(qa,'//*/div[@class="a-fixed-left-grid-col a-col-right"]/span[@class="askExpanderContainer noScriptNotDisplayExpander"]/span[@class="askLongText"]',text = True) #简短回答的详细回答
            data['qa_avatar'] = gethttp(get_xpath(qa, '//*[@class="a-profile-avatar"]/img', 'src'))  #头像
            data['qa_username'] = get_xpath(qa,'//*[@class="a-profile-name"]',text = True )  # 用户名
            data['qa_date']  = get_xpath(qa, '//*[@class="a-color-tertiary aok-align-center"]',text = True ) #日期
            data['qa_count'] = get_xpath(qa, '//*[@class="count"]', text = True)  #qa得票
            data['qa-detail_url'] = get_xpath(qa,'.a-link-normal:has-text("See all ")','href',is_text=True) #qa详情url
            # print(f'当前列表页线程id是{threading.current_thread().ident}')
            if data['qa_question']:
                result = mysql.submit_item(data, redis_key)  #用问题校验
                if result and data['qa-detail_url']:
                    detail_list.append(data) #此处要讲数据先保存到列表中，不然循环没结束就跳转页面，跳转页面内完成操作后回来就傻眼了，啥数据都拿不到了，因为页面变了。所以先拿数据在跳转
        for data in detail_list:
            get_qa_detail_data(page,asin,f'https://www.amazon.com{data["qa-detail_url"]}')  #跳转到qa详情页

        if next_page:
            get_data(page,asin,url = f'https://www.amazon.com{next_page}')
    except Exception as e:
        traceback.print_exc()
        print(f'qa获取出错啦{url}---{e}')

def get_qa_detail_data(page,asin,url):
    try:
        page.goto(url)  #["commit", "domcontentloaded", "load", "networkidle"]
        qa_list =  page.query_selector_all('.a-section.a-spacing-large.askAnswersAndComments.askWrapText > div')
        qa_question = get_xpath(page,'//*[@class="a-size-large askAnswersAndComments askWrapText"]/span',text=True)
        good_name = get_xpath(page,'//*[@class="a-size-base a-link-normal"]/p',text=True)
        for qa in qa_list:
            data = {}
            data['qadetail_asin_id'] = asin
            data['qadetail_url'] = url #qa详情url
            data['qadetail_question'] = qa_question #问题
            data['qadetail_good_name'] = good_name  #商品名
            data['qadetail_avatar'] = gethttp(get_xpath(qa,'//*[@class="a-profile-avatar"]/img','src')) # 头像
            data['qadetail_answer'] = get_xpath(qa, 'span',text=True )  #回答内容  !!!!!!!!!这里的bug就是qa本身就是个节点了，再获取只能获取向下的节点内容，不能再包含本身啦！！！
            data['qadetail_username'] = get_xpath(qa, '//*[@class="a-profile-name"]',text=True )  #用户名
            data['qadetail_date'] = get_xpath(qa, '//*[@class="a-color-tertiary aok-align-center"]',text=True )  #日期
            helpful = get_xpath(qa, '//*[@class="a-color-tertiary askVoteAnswerTextWithCount"]',text=True )
            if helpful:
                data['qadetail_helpful'] = helpful  #help count
            else:
                data['qadetail_helpful'] = 'Do you find this helpful?'
            if data['qadetail_answer']: mysql.submit_item(data, redis_detail_key)  # 用回答校验
            # print(f'当前详情页线程id是{threading.current_thread().ident}')

        detail_next_page = get_xpath(page, 'text=Next', 'href', is_text=True)  # 获取下一页的链接，没有说明没有下一页
        if detail_next_page:
            get_qa_detail_data(page,asin,url = f'https://www.amazon.com{detail_next_page}')
    except Exception as e:
        traceback.print_exc()
        print(f'qa获取出错啦{url}---{e}')


def get_xpath(page,xpath,attribute = '',text = False,is_text = False):
    '''默认是通过xpath获取属性的 text为true获取文本  is_test为True是通过文本查找获取属性或文本
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

def gethttp(url):
    '''判断图片中是否含有http,没有就添加一个前缀'''
    if url.find('http') == -1:
        return f'https://www.amazon.com{url}'



with sync_playwright() as playwright:
    run(playwright)
