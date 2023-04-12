# filter_links.py
# 用于把zhihu_valid_links中的纯链接搞到need_links.txt里


with open('zhihu_valid_links.txt','r',encoding='utf-8') as fr:
    lines = fr.readlines()
    lines = [line.strip() for line in lines]
    lines = [x for x in lines if x] #去掉空的
    lines = [x.split('|*|') for x in lines] #去掉分隔符

#原作者有一个判回答数的 我们暂时不需要

links_need = [x[0] for x in lines]
with open('need_links.txt','w') as fw:
    for item in links_need:
        fw.write(item + '\n')
