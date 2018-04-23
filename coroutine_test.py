#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lzx'

def consumer():
    r = ''
    while True:
        n = yield r  #接受调用者（produce）发送的数据
        if not n:
            return
        print('[CONSUMER] Consumer %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)        # 这个语句必须写，而且参数固定，作用是启动上面的生成器
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)     # 发送数据，生成器(consumer)接受数据，赋值给n变量
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)