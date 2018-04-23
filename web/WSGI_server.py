#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lzx'

from wsgiref.simple_server import make_server
#从hello.py导入自己编写的application函数
from hello import application

#创建一个服务器，IP地址为空，端口是8000，处理函数是application
httpd = make_server('', 8000, application)
print('Server HTTP on port 8000...')

#开始监听HTTP请求
httpd.serve_forever()
