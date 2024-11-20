# import re
# from playwright.sync_api import Playwright, sync_playwright, expect
#
#
# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("http://172.20.21.54:8088/jxgzWeb/#/")
#     page.locator("input[name=\"username\"]").click()
#     page.locator("input[name=\"username\"]").fill("zgdw29022")
#     page.locator("input[name=\"password\"]").dblclick()
#     page.locator("input[name=\"password\"]").fill("1qaz2wsx3edc$")
#     page.get_by_role("button", name="登录").click()
#     page.get_by_text("绩效工资申报").click()
#     page.get_by_role("menuitem", name="数据校验并上报").click()
#     page.get_by_role("button", name="数据校验并上报").click()
#     page.get_by_role("button", name="上报", exact=True).click()
#
#     # ---------------------
#     context.close()
#     browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)
from playwright.sync_api import Playwright, sync_playwright, TimeoutError


def run(playwright: Playwright) -> None:
    # 启动浏览器
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        # 打开目标页面
        page.goto("http://172.20.21.54:8088/jxgzWeb/#/")

        # 输入用户名和密码
        page.locator("input[name=\"username\"]").click()
        page.locator("input[name=\"username\"]").fill("zgdw29022")
        page.locator("input[name=\"password\"]").dblclick()
        page.locator("input[name=\"password\"]").fill("1qaz2wsx3edc$")

        # 点击登录按钮
        page.get_by_role("button", name="登录").click()
        page.wait_for_load_state("networkidle")  # 确保页面加载完成

        # 导航到“绩效工资申报”
        page.get_by_text("绩效工资申报").click()

        # 点击“数据校验并上报”
        page.get_by_role("menuitem", name="数据校验并上报").click()
        page.get_by_role("button", name="数据校验并上报").click()

        # 检查是否有错误提示
        try:
            error_message = page.locator("css=div.error-message").text_content(timeout=5)
            print(error_message+"dasdsad")
            if error_message:
                print(f"校验失败：{error_message}")
                return
        except TimeoutError:
            print("未检测到错误提示，继续操作...")

        # 如果没有错误，点击“上报”
        page.get_by_role("button", name="上报", exact=True).click()

        # 校验上报成功
        try:
            success_message = page.locator("css=div.success-message").text_content(timeout=5)
            print(f"上报成功：{success_message}")
        except TimeoutError:
            print("未检测到成功提示，上报可能失败。")

    except Exception as e:
        print(f"执行过程中发生错误：{e}")

    finally:
        # 关闭上下文和浏览器
        input('1..')
        context.close()
        browser.close()


with sync_playwright() as playwright:
    run(playwright)
