#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:phantomjs无界面浏览器+selenium
	Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
		http://blog.csdn.net/tcorpion/article/details/70213435
	State：
	Date:2017/4/28
	Author:tuling56
'''
import re, os, sys
import hues
import time
import random

reload(sys)
sys.setdefaultencoding('utf-8')

import headers
from selenium import  webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities   # 设置兼容性
from selenium.webdriver.common.proxy import ProxyType
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


'''
	phantomjs无界面浏览器
'''
class mPhantonJS():
	'''
		注意driver的关闭和退出
	'''
	def __init__(self):
		try:
			if False:
				self.driver=webdriver.PhantomJS(desired_capabilities=self.__webdrive_conf())
			else:
				self.driver=webdriver.PhantomJS() #executable_path=""
		except Exception,e:
			self.driver.quit()
			self.driver.close()

		self.driver.get('http://www.baidu.com/')

	def __del__(self):
		self.driver.quit()
		self.driver.close()


	# 请求配置
	def __webdrive_conf(self,imgload=False,isproxy=False):
		desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
		# 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
		desired_capabilities["phantomjs.page.settings.userAgent"] = (random.choice(headers.headers))

		#  不载入图片，爬页面速度会快很多
		if imgload:
			desired_capabilities["phantomjs.page.settings.loadImages"] = True
		else:
			desired_capabilities["phantomjs.page.settings.loadImages"] = False

		# 设置代理
		if isproxy:
			# 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
			proxy = webdriver.Proxy()
			proxy.proxy_type = ProxyType.MANUAL
			proxy.http_proxy = random.choice(headers.proxy_ips)
			proxy.add_to_capabilities(desired_capabilities)

		return desired_capabilities

	# 演示
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


