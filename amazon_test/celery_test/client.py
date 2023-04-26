# from celery_test import task1
# from celery_test import task2
from playwright.sync_api import Playwright, sync_playwright, expect
from amazon_detail import AmazonDetail
from amazon_detail import AmazonDetail
asin_list = ["B07PBFNYXV","B0B8ZD47L8","B0074UZV2G","B06ZYNZ7NF","B074H73B2K","B00GSL2RRO","B074H5SR5S","B00G0JHHNS","B00UJAJ2IM","B00PGXQ68Q","B0BWBP3T8B","B07FW6T2PW","B00LEXYEK4",
            "B000LKZ3GA","B00GSL34KI","B00VTR0UFI","B07NW4GSSR","B09DMV2XFX"]

amazon = AmazonDetail()
for i in range(len(asin_list)):
    if i % 2 == 0:
        res1 = amazon.get_data.delay(amazon,asin = asin_list[i])       # 或者 task1.add.apply_async(args=[2, 8])
    else:
        res2 = amazon.get_data.delay(asin = asin_list[i])  # 或者 task2.multiply.apply_async(args=[3, 7])
    print('hello world')



from functools import wraps
def dec(f):
    @wraps(f)
    def inner(a):
        f(a)
    return inner
@dec
def fun():
    print(1)