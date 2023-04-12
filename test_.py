#test_.py 用于测试每个模块
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
def get_user_info(user_url): # 用户主页url
    driverfile_path = r'D:\Computer_Science\Code\spider\zhihu_spider_for_wanliu\Driver\chromedriver.exe'
    # 启动浏览器
    driver2 = webdriver.Chrome(executable_path=driverfile_path)
    # 浏览器最大化
    driver2.maximize_window()
    # 打开百度首页
    driver2.get(user_url)
    # 隐式等待
    driver2.implicitly_wait(10)
    time.sleep(random.uniform(3, 4))
    # 定位登录界面关闭按钮
    close_btn = driver2.find_element(By.XPATH, "//button[@class='Button Modal-closeButton Button--plain']")
    # 点击登录界面关闭按钮
    close_btn.click()
    print('正在获取用户地址')
    # 定位用户ip地址
    user_ip = driver2.find_element(By.XPATH, "//div[@class='UserCover-ipInfo']").text  # 获取用户地址
    print(user_ip)
    return user_ip

author_url = 'https://www.zhihu.com/people/3p-53'
if author_url != 'https://www.zhihu.com/people/':
    try:
        user_ip = get_user_info(author_url)
    except Exception as e:  # 这种情况下多半是账号被注销了
        user_ip = ''
        print('该账号可能被注销')