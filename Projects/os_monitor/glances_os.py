#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:glances XML/RPC API调用接口
	Ref:
		http://www.tuicool.com/articles/rMjIju
		http://www.cnblogs.com/coderzh/archive/2008/12/03/1346994.html （自定义服务器端的方法）
		https://github.com/nicolargo/glances/wiki/The-Glances-2.x-API-How-to （推荐使用）
	State：进行中
	Date:2017/3/31
	Author:tuling56
'''
import re, os, sys
import hues
import glances
import xmlrpclib   #这个库的作用是什么？？

reload(sys)
sys.setdefaultencoding('utf-8')


def mglances():
	s = xmlrpclib.ServerProxy('http://10.10.160.11:61209')
	print s.getSystem()    #怎么知道s有哪些方法




if __name__ == "__main__":
	mglances()

