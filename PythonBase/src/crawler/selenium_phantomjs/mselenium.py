#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:web自动化测试工具selenium
	Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
	State：
	Date:2017/4/28
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import  webdriver

def fun():
	driver = webdriver.PhantomJS()    # 获取浏览器对象
	driver.get('http://www.baidu.com/')
	print driver.page_source


if __name__ == "__main__":
	fun()

