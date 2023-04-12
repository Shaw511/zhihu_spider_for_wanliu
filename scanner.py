#scanner.py
import requests
import random
from time import sleep
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

'''
下面这段用于接着刚才的zhihu_valid_links.txt的link接着读
'''

with open('zhihu_valid_links.txt','r',encoding='utf-8') as f:
    data = f.readlines()[-1] #最后一个有效格式链接
    print(data)
    zhihu_link = data.split('|*|')[0]
    number = int(zhihu_link.split('/')[-1].strip()) #问题id
    # print(number)

number = 575643737 #问题id
num_need = 1
num_end = number + num_need
print(f'from question {number} to question {num_end}')
while number <= num_end:
    #随机休息
    time_sleep = random.uniform(3,4)
    sleep(time_sleep)

    url = 'https://www.zhihu.com/question/'+str(number)

    #网络错误情况处理
    try:
        response = requests.get(url,headers=headers)
    except Exception as e:
        print('**')
        time_sleep = random.uniform(300,600)
        print(f'网络错误，暂停{time_sleep}s:',e)
        sleep(time_sleep)
        print('question id:', number, ';error:',e)
        number -= 1
        continue

    print(url)
    # print(response.text)
    # print(response.status_code)
    if response.status_code == 200:
        if '你似乎来到了没有知识存在的荒原' in response.text:
            # print('是')
            continue
        else:
            title = re.findall('<title data-rh="true">(.*)</title>',response.text)[0] #正则表达式清洗出title
            print('title:',title)
            try:
                num_answer = re.findall('<span>(.*)<!-- --> 个回答</span>',response.text)[0]
            except Exception as e: #一般是没有回答的问题
                num_answer = 0
            print('num_answer:',num_answer)
            with open('zhihu_valid_links.txt','a',encoding='utf-8') as f:
                f.write(url + '|*|' + title + '|*|' + str(num_answer)+'\n')

            print(url)
            print('--')
    else:
        print('question id:', number, ';error code:', response.status_code)

    number = number + 1
