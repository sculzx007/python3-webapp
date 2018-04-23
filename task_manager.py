#! /usr/bin/env python3
#-*- coding:utf-8 -*-
#分布式进程

import random, time, queue
from multiprocessing.managers import BaseManager

#发送任务的队列
task_queue = queue.Queue()

#接收结果的队列
result_queue = queue.Queue()

#从BaseManager继承的QueueManager
class QueueManager(BaseManager):
    pass

#由于window中，callable后面不支持匿名函数，故将廖雪峰代码处的callable=lambda: task_queue改为以下函数
def taskQueue():
    return task_queue

def resultQueue():
    return result_queue
#把两个Queue都注册到网络上，callable参数关联了Queue对象
QueueManager.register('get_task_queue', callable=taskQueue)
QueueManager.register('get_result_queue', callable=resultQueue)

#绑定端口5000，设置验证码为‘abc’
manager = QueueManager(address=('127.0.0.1', 5000), authkey= b'abc')

#启动Queue
manager.start()

#获得通过网络访问的Queue对象
task = manager.get_task_queue()
result = manager.get_result_queue()

#放几个任务进去
for i in range(10):
    n = random.randint(0, 10000)
    print('Put task %d...' % n)
    task.put(n)

#从result队列读取结果
print('Try get results...')
for i in range(10):
    r = result.get(timeout = 10)
    print('Result: %s' % r)

#关闭
manager.shutdown()
print('master exit')
