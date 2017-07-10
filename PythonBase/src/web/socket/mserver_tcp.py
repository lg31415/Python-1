#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:socket tcp通信-服务器端
    Ref:http://www.cnblogs.com/nzyjlr/p/4236287.html
    State：
    Date:2016/11/6
    Author:tuling56
'''
import os,sys,re
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


import socket
import time
import threading

'''
	创建服务器端连接
'''
def tcplink(sock,addr):
    hues.info("accept new connection from %s:%s..." % addr)
    sock.send("Welcom!".encode())
    while True:                 #通信循环：发送与接收
        data=sock.recv(1024)
        hues.success("Received [%s] from %s:%s" %(data,addr[0],addr[1]))
        time.sleep(2)
        if data=='exit' or not data:
            break
        sock.send("hello: ".encode()+data)
    sock.close()
    hues.warn("Connection from %s:%s closed." % addr)


'''
	tcp服务器（多线程）
'''
def tcpserver():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 创建一个基于ipv4 的TCP协议的socket
#    s.bind(('127.0.0.1',9999))
    s.bind(('127.0.0.1',80))
    s.listen(5)                 # 开始监听
    hues.log("Waiting for connection......")
    # 无限循环等待连接
    while True:
        sock,addr=s.accept()   # 返回一个单独的新的客户端套接字用来处理
        t=threading.Thread(target=tcplink,args=(sock, addr))
        t.start()

# 测试入口
if __name__ == "__main__":
    tcpserver()

