import time

from playwright.sync_api import Playwright, sync_playwright
import json
import re

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    # 加载状态
    with open("state.json") as f:
        storage_state = json.loads(f.read())
    context = browser.new_context(storage_state=storage_state)
    page = context.new_page()
    page.goto("https://yuyues.hnmuseum.com/w/personal/order/chooseDate?type=1&stack-key=17d5a71d")

    page.query_selector().click()
    page.get_by_text("09:00-12:00基临").click()
    page.locator("i").click()
    while True:
        page.get_by_text("下一步").click()

    page.get_by_text("+ 请选择观众").click()
    page.get_by_role("listitem").filter(has_text="李双博身份证231084199305233713").locator("a").first.click()
    page.get_by_text("确定选择").click()
    page.get_by_role("listitem").filter(has_text="与天无极 璀璨秦中——陕西周秦汉唐文物精华展详情有票￥50").locator("a").click()
    page.get_by_text("下一步").click()
    page.get_by_text("提交预约").click()
    time.sleep(500)

    page.close()
    context.close()
    browser.close()

    # storage = context.storage_state()    #登录后保存cookie
    # with open("state.json", "w") as f:
    #     f.write(json.dumps(storage))

with sync_playwright() as playwright:
    run(playwright)