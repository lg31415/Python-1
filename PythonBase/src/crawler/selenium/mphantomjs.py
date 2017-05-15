#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:phantomjs无界面浏览器+selenium
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
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

'''
	phantomjs无节面浏览器
'''
class mPhantonJS():
	def __init__(self):
		try:
			self.driver=webdriver.PhantomJS()
		except Exception,e:
			self.driver.quit()
			return False

		self.driver.get('http://www.baidu.com/')

	def demo(self):
		print self.driver.title #,driver.page_source
		assert "百度" in self.driver.title
		elem=self.driver.find_element_by_id("kw")
		elem.send_keys("张二狗"+Keys.RETURN)
		time.sleep(2)
		try:
			#driver.find_element_by_name()
			assert '张二狗' in self.driver.title
			print self.driver.title
			print self.driver.page_source.encode('utf8')
		except NoSuchElementException:
			assert 0,u"找不到搜索的元素"
		self.driver.close()
		self.driver.quit()

# 测试入口
if __name__ == "__main__":
	mpjs=mPhantonJS()
	mpjs.demo()


