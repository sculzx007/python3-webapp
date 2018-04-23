#! /usr/bin/env python3
#-*- coding:utf-8 -*-

#作为UDP客户端
import socket

#新建一个连接
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for data in [b'Liu', b'Waang', b'Li']:
    #发送数据
    s.sendto(data, ('127.0.0.1', 9999))

    #接收数据
    print(s.recv(1024).decode('utf-8'))

s.close()