#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lzx'

#利用async和await进行重写，获取sina、sohu和163的网站首页

'''
async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：
1. 把@asyncio.coroutine替换为async；
2. 把yield from替换为await。
'''
import asyncio

async def wget(host):
    print('Wget %s...' % host)

    #利用协程，创建一个连接
    connect = asyncio.open_connection(host, 80)
    reader, writer  = await connect                    # 这个io操作比较耗时，所以会执行下个协程

    #给连接一个请求头header
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host     #当遇到连续两个\r\n（\r\n\r\n）时，表明header部分结束，后面的都是body
    writer.write(header.encode('utf-8'))

    await writer.drain()                                # 刷新底层传输的写缓冲区。也就是把需要发送出去的数据，从缓冲区发送出去。
    while True:
        line = await reader.readline()                 # 这个io操作有时不耗时，会直接运行整个循环
        if line == b'\r\n':                                  #每个header一行一个，换行符是\r\n
            break
        print('%s header >> %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()                                          #无视网页的body部分，直接关闭writer

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(task))
    loop.close()


