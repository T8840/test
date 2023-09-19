# # Terminal: playwright codegen demo.playwright.dev/todomvc


# from playwright.sync_api import Playwright, sync_playwright, expect


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://demo.playwright.dev/todomvc/")
#     page.goto("https://demo.playwright.dev/todomvc/#/")
#     page.get_by_placeholder("What needs to be done?").click()
#     page.get_by_placeholder("What needs to be done?").fill("123")
#     page.get_by_text("This is just a demo of TodoMVC for testing, not the real TodoMVC app. todos Doub").click()
#     page.get_by_text("Double-click to edit a todo").click()
#     page.get_by_text("Double-click to edit a todo").dblclick()
#     page.get_by_text("Part of TodoMVC").click()

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)



from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://baidu.com/")
    page.goto("http://www.baidu.com/")
    page.locator("#kw").click()
    page.locator("#kw").fill("123")
    page.get_by_role("button", name="百度一下").click()
    page.locator("#content_left [id=\"\\31 \"]").get_by_role("link", name="hao123_上网从这里开始").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)