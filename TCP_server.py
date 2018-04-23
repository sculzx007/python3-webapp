#! /usr/bin/env python3
#-*- coding:utf-8 -*-

#作为服务器端
import socket, threading, time


#每个新连接都需要创建新线程（或进程）来处理，否则无法同时接收多个客户端的连接请求
def link(sock, addr):
    print('Accept new connection from %s: %s' % addr)
    sock.send(b'Welcome!')

    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send('Hello, %s!' % data).encode('utf-8')

    sock.close()
    print('Connection from %s: %s closed' % addr)


#创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#绑定端口
s.bind(('127.0.0.1', 9999))               #127.0.0.1表示本机端口

#监听端口
s.listen(5)                              #表示指定等待连接的最大数量
print('Waiting for connection...')

while True:
    #接受一个新连接
    sock, addr = s.accept()

    #创建新线程来处理TCP连接
    t = threading.Thread(target=link, args=(sock, addr))
    t.start()


