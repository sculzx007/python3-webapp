#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lzx'

#练习协程

import asyncio, threading

@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.current_thread())

    #异步调用generator asyncio.sleep（）
    # yield form 语句返回的值是后面表达式迭代后遇到StopIteration后再return（这个语句） 的值，无这个语句是返回None
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.current_thread())

#获取EventLoop
loop = asyncio.get_event_loop()

#执行coroutine
task = [hello(), hello()]

#wait()是将参数里的协程转为一个包括他们在内的单独协程
loop.run_until_complete(asyncio.wait(task))
loop.close()
