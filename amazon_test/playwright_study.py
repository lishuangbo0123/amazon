import time
from playwright.sync_api import Playwright, sync_playwright, expect
from pipeline import MySQLPipline
import re

# 不加载图片
def cancel_request(route, request):
    route.abort()

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(geolocation={"latitude": 34.1227, "longitude": 118.7573}, locale="en-UA",permissions=["geolocation"], timezone_id="America/Los_Angeles")
    # context = browser.new_context()
    page = context.new_page()
    # page.on('response', on_response)
    # page.screenshot(path='location-iphone.png')
    page.wait_for_load_state('networkidle')
    page.goto("https://www.amazon.com/dp/B07PBFNYXV/ref=sr_1_1_sspa")
    # page.route(re.compile(r"(.png)|(.jpg)"), cancel_request)
    data = {}
    data['image'] = get_xpath(page,"//*[contains(@class,'imgTagWrapper')]/img",'src')  #主图
    data['ratings'] = get_xpath(page,'//*[@id="acrCustomerReviewText"]',is_text=True)   # 评论数
    data['answered_questions'] = get_xpath(page,'//*[@id="askATFLink"]/span',is_text=True)  # qa数量
    data['brand'] = get_xpath(page,'//*[@id="bylineInfo"]',is_text=True) #跟卖链接
    data['star_avg'] = get_xpath(page,'//*[@id="reviewsMedley"]//div[@class="a-row"]/span[@class="a-size-base a-nowrap"]/span[@data-hook="rating-out-of-text"]',is_text=True) # 星评
    data['comment_url'] = get_xpath(page,'//*[@id="reviews-medley-footer"]/div[2]/a','href')
    data['qa_url'] = get_xpath(page,'//*[@class ="a-button a-button-base askSeeMoreQuestionsLink"]/span/a','href')
    print(data)
    context.close()
    browser.close()

def get_xpath(page,xpath,attribute = '',is_text = False):
    if is_text:
        if page.query_selector(xpath):
            return page.query_selector(xpath).text_content()
        else:
            return ''
    else:
        if page.query_selector(xpath):
            return page.query_selector(xpath).get_attribute(attribute)
        else:
            return ''


def on_response(response):
    if 'ref=sr_1_1_sspa' in response.url and response.status == 200:
        pass



with sync_playwright() as playwright:
    run(playwright)



# 翻译插件
# def plugin_translate(self, text: str, language: str = 'zh-CN'):
#     '''
#     :param text: 要翻译的内容，来源语种自动识别
#     :param language:de：德语,ja：日语,sv：瑞典语,nl：荷兰语,ar：阿拉伯语,ko：韩语,pt：葡萄牙语,zh-CN：中文简体,zh-TW：中文繁体
#     :return:翻译后的文本
#     '''
#     ctx = execjs.compile("""
#         function TL(a) {
#             var k = "";
#             var b = 406644;
#             var b1 = 3293161072;
#             var jd = ".";
#             var $b = "+-a^+6";
#             var Zb = "+-3^+b+-f";
#             for (var e = [], f = 0, g = 0; g < a.length; g++) {
#                 var m = a.charCodeAt(g);
#                 128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
#                 e[f++] = m >> 18 | 240,
#                 e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
#                 e[f++] = m >> 6 & 63 | 128),
#                 e[f++] = m & 63 | 128)
#             }
#             a = b;
#             for (f = 0; f < e.length; f++) a += e[f],
#             a = RL(a, $b);
#             a = RL(a, Zb);
#             a ^= b1 || 0;
#             0 > a && (a = (a & 2147483647) + 2147483648);
#             a %= 1E6;
#             return a.toString() + jd + (a ^ b)
#         };
#         function RL(a, b) {
#             var t = "a";
#             var Yb = "+";
#             for (var c = 0; c < b.length - 2; c += 3) {
#                 var d = b.charAt(c + 2),
#                 d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
#                 d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
#                 a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
#             }
#             return a
#         }
#     """)
#     try:
#         text = text.strip().replace('"', '\"').replace("'", '\'').replace('!', '！').replace('\n', ' ')
#         url = f'https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl={language}&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&source=btn&ssel=0&tsel=0&kc=0&tk={str(ctx.call("TL", text))}&q={quote(text, encoding="utf-8")}'
#         headers = {
#             'authority': 'translate.google.cn',
#             'method': 'GET',
#             'path': url.replace('https://translate.google.cn', ''),
#             'scheme': 'https',
#             'accept': '*/*',
#             'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
#             'referer': 'https://translate.google.cn/',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
#         }
#         res = requests.get(url, headers=headers)
#         res_list = json.loads(res.text)
#     except:
#         return f'翻译失败：请求失败'
#     try:
#         return ''.join([i[0] for i in res_list[0][:-1]])
#     except:
#         return f'翻译失败：找不到翻译内容{res_list}'