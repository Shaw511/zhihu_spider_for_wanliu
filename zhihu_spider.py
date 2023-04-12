# -*- coding: utf-8  -*-

import datetime
import time, json, re
from time import sleep
import pandas as pd
import config
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_html(url):
    # 填写chromedriver.exe的路径
    driverfile_path = r'D:\Computer_Science\Code\spider\zhihu_spider_for_wanliu\Driver\chromedriver.exe'
    # 启动浏览器
    driver = webdriver.Chrome(executable_path=driverfile_path)
    # 浏览器最大化
    driver.maximize_window()


    # driver = get_driver(url)
    # 隐式等待
    driver.implicitly_wait(10)
    # 浏览器最大化
    driver.maximize_window()
    driver.get(url)
    time.sleep(random.uniform(3, 4))
    # 定位登录界面关闭按钮
    close_btn = driver.find_element(By.XPATH, "//button[@class='Button Modal-closeButton Button--plain']")
    # 点击登录界面关闭按钮
    close_btn.click()  # 获取当前窗口的总高度
    js = 'return action=document.body.scrollHeight'
    # 初始化滚动条所在的高度
    height = 0
    # 当前窗口总高度
    currHeight = driver.execute_script(js)
    while height < currHeight:
        # 将滚动条调整至页面底端
        for i in range(height, currHeight, 100):
            driver.execute_script("window.scrollTo(0, {})".format(i))
            time.sleep(0.02)
        height = currHeight
        currHeight = driver.execute_script(js)
        time.sleep(3)

    # scroll_to_bottom(driver)
    answerElementList = driver.find_elements(By.CSS_SELECTOR, "#QuestionAnswers-answers .List-item .ContentItem")
    return answerElementList, driver

def get_user_info(user_url,driver): # 用户主页url
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

def scroll_to_bottom(driver):
    # 获取当前窗口的总高度
    js = 'return action=document.body.scrollHeight'
    # 初始化滚动条所在的高度
    height = 0
    # 当前窗口总高度
    currHeight = driver.execute_script(js)
    while height < currHeight:
        # 将滚动条调整至页面底端
        for i in range(height, currHeight, 100):
            driver.execute_script("window.scrollTo(0, {})".format(i))
            time.sleep(0.02)
        height = currHeight
        currHeight = driver.execute_script(js)
        time.sleep(3)


def get_answers(answerElementList, url,driver):
    # 定义一个存储回答中的信息的数据表格
    answerData = pd.DataFrame(
        columns=(
            'question_title', 'answer_url', 'question_url', 'author_name', 'author_url','fans_count', 'created_time', 'updated_time',
            'comment_count','voteup_count', 'content'))
    numAnswer = 0
    # 遍历每一个回答并获取回答中的信息
    for answer in answerElementList:
        dictText = json.loads(answer.get_attribute('data-zop'))
        question_title = dictText['title']  # 问题名称
        answer_url = answer.find_element(By.XPATH,
                                         "meta[@itemprop='url' and contains(@content, 'answer')]").get_attribute(
            'content')  # 获取回答的链接
        author_name = dictText['authorName']  # 回答作者名称

        author_url = answer.find_element(By.XPATH,"*//meta[contains(@itemprop,'url')]").get_attribute(
            'content')
        print(author_url) #获取作者主页链接

        if author_url != 'https://www.zhihu.com/people/':
            try:
                user_ip = get_user_info(author_url,driver)
            except Exception as e: #这种情况下多半是账号被注销了
                user_ip = ''
                print('该账号可能被注销')
        #匿名用户ip的抓取
        fans_count = answer.find_element(By.XPATH, "*//meta[contains(@itemprop, 'followerCount')]").get_attribute(
            'content')  # 获取粉丝数量
        created_time = answer.find_element(By.XPATH, "meta[@itemprop='dateCreated']").get_attribute(
            'content')  # 获取回答的创建时间
        updated_time = answer.find_element(By.XPATH, "meta[@itemprop='dateModified']").get_attribute(
            'content')  # 获取回答最近的编辑时间
        comment_count = answer.find_element(By.XPATH, "meta[@itemprop='commentCount']").get_attribute(
            'content')  # 获取该回答的评论数量
        voteup_count = answer.find_element(By.XPATH, "meta[@itemprop='upvoteCount']").get_attribute(
            'content')  # 获取回答的赞同数量
        contents = answer.find_elements(By.TAG_NAME, "p")# .text.replace("\n", "")  # 回答内容
        content = ''.join([content.text for content in contents])
        print(content)


        time.sleep(0.001)
        row = {'question_title': [question_title],
               'author_name': [author_name],
               'author_url':[author_url],
               'author_ip':[user_ip],
               'question_url': [url],
               'answer_url': [answer_url],
               'fans_count': [fans_count],
               'created_time': [created_time],
               'updated_time': [updated_time],
               'comment_count': [comment_count],
               'voteup_count': [voteup_count],
               'content': [content]
               }
        answerData = answerData.append(pd.DataFrame(row), ignore_index=True)
        numAnswer += 1
        print(f"[NORMAL] 问题：【{question_title}】 的第 {numAnswer} 个回答抓取完成...")
        time.sleep(0.2)

    return answerData, question_title


if __name__ == '__main__':
    # 获取当前已经抓取的所有问题
    try:
        df_tmp = pd.read_csv('zhihu_result.csv')
        question_url_contained = set(df_tmp['question_url'].to_list())
        print('已经抓取的代码')
        print(question_url_contained)#已经存在问题得url
        del df_tmp

    except Exception as e:
        print('no breakpoint:', e)
        question_url_contained = set()
        # 创建表头
        answerData_init = pd.DataFrame(
            columns=(
                'question_title','answer_url', 'question_url', 'author_name', 'author_url', 'fans_count', 'created_time', 'updated_time',
                'comment_count',
                'voteup_count', 'content','author_ip'))
        answerData_init.to_csv(f'zhihu_result1.csv', mode='a', encoding='utf-8', index=False, header = True)

    print('需要抓取的问题数量：', len(config.urls)) # 从config里面获取url
    for url in config.urls:#开始遍历urls
        if url in question_url_contained:#代表已经抓取过了
            continue#跳过
        print('----------------------------------------')
        print('url:', url)
        #'https://www.zhihu.com/question/313421184'
        url_num = int(url.split('/')[-1])

        try:
            # time.sleep(random.uniform(60, 120)) #先把推迟去掉 待会正式运行的时候加上

            #time.sleep(t)表示推迟线程得运行
            #random.uniform(参数1，参数2) 返回参数1和参数2之间的任意值
            answerElementList, driver = get_html(url)
            print("[NORMAL] 开始抓取该问题的回答...")
            answerData, question_title = get_answers(answerElementList, url,driver)
            print(f"[NORMAL] 问题：【{question_title}】 的回答全部抓取完成...")
            time.sleep(random.uniform(1, 3))
            question_title = re.sub(r'[\W]', '', question_title)
            filename = str(f"result-{datetime.datetime.now().strftime('%Y-%m-%d')}-{question_title}")
            answerData.to_csv(f'zhihu_result1.csv', mode='a', encoding='utf-8', index=False, header = False)
            print(f"[NORMAL] 问题：【{question_title}】 的回答已经保存至 {filename}.xlsx...")
            time.sleep(random.uniform(1,3))
            driver.close()
            # print(e)
            # print(f"[ERROR] 抓取失败...")
        except Exception as e:
            # time.sleep(random.uniform(300, 400)) #先注释掉 等正式运行再加上
            print(e)
            print(f"[ERROR] 抓取失败...")
            continue
