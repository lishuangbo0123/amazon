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
    time.sleep(20)
    storage = context.storage_state()  # 登录后保存cookie
    with open("state.json", "w") as f:
        f.write(json.dumps(storage))

    page.close()
    context.close()
    browser.close()



with sync_playwright() as playwright:
    run(playwright)