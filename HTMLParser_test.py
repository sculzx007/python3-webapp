#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):   #处理开始标签
        print('<%s>' % tag)
    def handle_endtag(self, tag):            #处理结束标签
        print('</%s>' % tag)
    def handle_startendtag(self, tag, attrs):         #处理单标签，例如<br/>
        print('<%s/>' % tag)
    def handle_data(self, data):              #处理标签里的内容
        print(data)
    def handle_comment(self, data):           #处理注释
        print('<!--', data, '-->')
    def handle_entityref(self, name):         #这个是处理特殊字符，比如&nbsp
        print('&%s;' % name)
    def handle_charref(self, name):           #这个是处理特殊字符，比如&#1234
        print('&#%s' % name)

if __name__ == '__main__':
    parser = MyHTMLParser()
    parser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
</body></html>''')

