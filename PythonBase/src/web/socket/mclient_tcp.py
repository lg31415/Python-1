#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:scoket tcp通信-客户端
	Ref:http://www.cnblogs.com/nzyjlr/p/4236287.html
	State：
	Date:2016/11/6
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


import hues
import socket

'''
	客户端程序TCP 连接
'''
def tcpclient():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(('10.10.160.11',9999))
	hues.info(s.recv(1024))
	for data in list('s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)'): #['Michael','Tracy','Sarah']:
		s.send(data.encode())
		print(s.recv(1024))
	s.send(b'exit')

if __name__ == "__main__":
	tcpclient()

