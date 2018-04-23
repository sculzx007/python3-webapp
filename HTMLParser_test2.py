#! /usr/bin/env python3
#-*- coding:utf-8 -*-

#作业：找一个网页，例如https://www.python.org/events/python-events/，用浏览器查看源码并复制，然后尝试解析一下HTML，输出Python官网发布的会议时间、名称和地点。
from html.parser import HTMLParser
from urllib import request
from pyquery import PyQuery as pq
import re

# 方法1
class MyHTMLParser(HTMLParser):
    flag = 0
    res = []
    is_get_data = 0

    def handle_starttag(self, tag, attrs):
        #首先找到包含有信息的标签
        if tag == 'ul':
            for attr in attrs:
                return attr[1]
                if re.match(r'list-recent-events menu', attr[1]):
#attrs是一个列表，其中每个元素是元组类型，所以用for att in attrs 会返回一个元组给att，att[0]表示的是属性名，att[1]表示的才是属性值
                    self.flag = 1

        #处理包裹事件名称的a元素
        if tag == 'a' and self.flag == 1:
            self.is_get_data = 'title'

        #处理包裹时间的time元素
        if tag == 'time' and self.flag == 1:
            self.is_get_data = 'time'

        #处理包裹地点的span元素
        if tag == 'span' and self.flag == 1:
            self.is_get_data = 'addr'

    def handle_endtag(self, tag):
        if self.flag == 1 and tag == 'ul':
            self.flag = 0

    def handle_data(self, data):
        if self.is_get_data and self.flag == 1:
            if self.is_get_data == 'title':
                self.res.append({self.is_get_data: data})
#获得title, 即会议名时，给res添加一个新dict：self.res.append({self.is_get_data: data}, res由[]变为[{'title': 'PyCascades 2018'}]

            else:
                self.res[len(self.res)-1][self.is_get_data] = data
#获得addr，time这样的其它属性时,先把最后一个dict（即当前处理的dict）取出：即self.res[len(self.res) - 1]
#再把新属性加入：self.res[len(self.res) - 1][self.is_get_data] = data
# [{'title':'PyCascades 2018','time':'22 Jan. – 24 Jan.'}]

            self.is_get_data = None



if __name__ == '__main__':
    url = 'https://www.python.org/events/python-events/'
    parser = MyHTMLParser()
    with request.urlopen(url) as f:
        data = f.read().decode('utf-8')

    parser.feed(data)
    for item in MyHTMLParser.res:
        print('------------')
        for k, v in item.items():
            print('%s: %s' % (k,v))

    #方法2

    doc = pq(url=url)
    events = doc('.shrubbery .list-recent-events.menu').text()

    print('Upcoming Events:')
    print('-------------------------------------------')
    print(events)