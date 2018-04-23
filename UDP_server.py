#! /usr/bin/env python3
#-*- coding:utf-8 -*-

#作为UDP服务器
import socket

#新建一个连接
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#绑定端口
s.bind(('127.0.0.1', 9999))

print('Bind UDP on 9999...')
while True:
    #接收数据
    data, addr = s.recvfrom(1024)       #recvfrom()返回的是数据和客户端的地址与端口
    print('Received from %s: %s' % addr)
    s.sendto(b'Hello, %s' % data, addr)
