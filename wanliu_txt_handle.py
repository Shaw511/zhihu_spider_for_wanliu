# 针对wanliu_result.txt文本文件的数据清洗 词云输出
# 词云输出到 万柳书院词云图.jpg
import jieba
import numpy
from PIL import Image
from wordcloud import WordCloud
import matplotlib.colors as colors

with open('wanliu_result.txt',encoding='utf-8') as f:
    lines = f.readlines()
txt = ''
for line in lines:
    txt += line
words = jieba.lcut(txt)
#汉语停用词清洗
with open('stoplist.txt',encoding='utf-8') as f2:
    lines2 = f2.readlines()
stop_list = []
for line in lines2:
    line = line.replace('\n','')
    stop_list.append(line)
# print(stop_list)
words_clean = []
# print(words)
for word in words:
    if word in stop_list:
        continue
    else:
        words_clean.append(word)
# print(txt)
print(words_clean)
newtxt = ''.join(words_clean)
color_mask = numpy.array(Image.open('rabbit.jpg')) #底图
colormaps = colors.ListedColormap(['#CD5C5C','#FA8072','#DB7093'])  #印度红 鲜肉(鲑鱼)色 苍白的紫罗兰红色
wordcloud = WordCloud(
    colormap=colormaps,
    font_path='C:\5c8a05e42d4d61552549348.ttf',
    # mask=color_mask,
    background_color='white',
    width=4096,
    height=4096
).generate(newtxt)
wordcloud.to_file('万柳书院词云图.jpg')