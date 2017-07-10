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
#	s.connect(('10.10.160.11',9999))
	s.connect(('127.0.0.1',80))
	hues.info(s.recv(1024))

	# 自动
	'''
	for data in ['Michael','Tracy','Sarah']: #list('s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)')
		s.send(data.encode())
		print(s.recv(1024))
	s.send(b'exit')
	'''

	# 交互
	while True:
		sd=raw_input("请输入要发送的内容:")
		s.send(sd.encode())
		print (s.recv(1024))
		if sd=='exit' or sd=='quit' or sd=='q':
			print "程序退出"
			break

# 测试入口
if __name__ == "__main__":
	tcpclient()

