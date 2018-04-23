#! /usr/bin/env python3
#-*- coding:utf-8 -*-

#分布式进程，处理分布式进程发送的数据
import time, sys, queue
from multiprocessing.managers import BaseManager

#创建类似的QueueManager
class QueueManager(BaseManager):
    pass

#由于这个QueueManager只能从网上（task_manager.py）获取，所以注册时只提供名字
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

#连接到服务器，也就是运行task_manager.py的机器
server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)

#端口验证注意与task_manager.py保持一致
m = QueueManager(address=(server_addr, 5000), authkey=b'abc')

#从网络连接
m.connect()

#获取Queue对象
task = m.get_task_queue()
result = m.get_result_queue()

#从task队列获取任务，并把结果写入result队列
for i in range(10):
    try:
        n = task.get(timeout=1)
        print('run task %d * %d' % (n, n))
        r = '%d * %d = %d' % (n, n, n * n)
        time.sleep(1)
        result.put(r)
    except queue.Empty:
        print('task queue is empty')

#处理结束
print('worker exit')
