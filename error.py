#! /usr/bin/env python3
#-*-coding:utf-8-*-
__author__ = 'lzx'
import logging

'''错误的处理，有五种方法
(1)使用print，将错误打印出来，但是不美观
（2）使用断言，assert，如果assert欧的判断语句为False，则抛出错误
（3）使用logging，不会抛出错误，而且可以输出到文件
（4）使用pdb模式
（5）使用idle自带的断点功能
'''
#第一种方法，使用print
def f1(s):
    n = int(s)
    print("n is zero")
    return 10/n
f1(0)

#第二种方法，使用断言，assert
def f2(s):
    n = int(s)
    assert n != 0, 'n is zero'
    print('aaa')
    return 10/n
f2(0)


#第三种方法，使用logging
def f3(s):
    n = int(s)
    logging.info('n = %d' % n)
    print('aaa')
    return 10/n
f3(0)

#第四种方法，使用pdb模式（程序单步运行），方法一是在命令行中输入 python3 -m pdb error.py，但是每运行一行代码，就需要输入一条命令
def f3(s):
    n = int(s)
    logging.info('n = %d' % n)
    print('aaa')
    #方法二，在可能出错的地方，加上代码 pdb.set_trace()
    return 10/n
f3(0)