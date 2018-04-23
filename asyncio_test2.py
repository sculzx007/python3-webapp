#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lzx'

#使用asyncio的异步网络连接来获取sina、sohu和163的网站首页

import asyncio

@asyncio.coroutine
def wget(host):
    print('Wget %s...' % host)

    #利用协程，创建一个连接
    connect = asyncio.open_connection(host, 80)
    reader, writer  = yield from connect                    # 这个io操作比较耗时，所以会执行下个协程

    #给连接一个请求头header
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host     #当遇到连续两个\r\n（\r\n\r\n）时，表明header部分结束，后面的都是body
    writer.write(header.encode('utf-8'))

    yield from writer.drain()                                # 刷新底层传输的写缓冲区。也就是把需要发送出去的数据，从缓冲区发送出去。
    while True:
        line = yield from  reader.readline()                 # 这个io操作有时不耗时，会直接运行整个循环
        if line == b'\r\n':                                  #每个header一行一个，换行符是\r\n
            break
        print('%s header >> %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()                                          #无视网页的body部分，直接关闭writer

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(task))
    loop.close()


    '''
    别人的理解：
    在 reader, writer = yield from connect这里，线程在执行connect操作，挂起，三个网站连接都被挂起，哪个先连接上，先有返回对象，行，sina的连接有返回对象了，通过reader，writer解包进行接下来的操作，只要碰到yield from就挂起，执行tasks里的别的连接任务。
感觉协程异步相比同步执行节省的时间是就是读取信息流，获得返回对象的时间。相比等待一个连接成功，然后进行操作，操作完继续进行另一个连接，节省的时间就在connect过程中，因为我把三个连接全部开启，谁连上获得对象我就接着执行谁。所以打印出的顺序会不一样。
相同的获取信息的例子就是把文件读取到内存中：
line = yield from reader.readline()这也要挂起，你读你的第一行，我继续读下一行。
同时我觉得yield from内部应该有个消息管道，获取到的信息按顺序排列。
    '''