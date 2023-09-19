import re
from playwright.sync_api import Page, expect

page = context.newPage()
def Whether_intercept() -> bool:
    return True  #进行拦截
# return False #不进行拦截

def handler(route:Route):
    print(route.request.url)
    #正常访问
    # route.continue_()
    #拒绝访问
    # route.abort("网络拦截")
    # 重定向到非目标地址
    route.fulfill(
        status=302,
        headers={
            'Location' : "https://xingzheai.cn/"
        }
    )
page.route(Whether_intercept,handler)