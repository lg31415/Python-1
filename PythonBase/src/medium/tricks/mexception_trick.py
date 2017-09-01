#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:提高Python运行效率的技巧
	Ref:http://python.jobbole.com/86308/
	Date:2016/9/9
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

def fun():
	n = 16
	myDict = {}
	for i in range(0, n):
		char = 'abcd'[i%4]
		if char not in myDict:
			myDict[char] = 0
		myDict[char] += 1
		print(myDict)

# 通过异常处理来提高运行效率
def fun_impl():
	n = 16
	myDict = {}
	for i in range(0, n):
		char = 'abcd'[i%4]
		try:
			myDict[char] += 1
		except KeyError:
			myDict[char] = 1
		print(myDict)


# 测试入口
if __name__ == "__main__":
    fun_impl()

