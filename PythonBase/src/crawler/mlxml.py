#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun: xpath语法测试
	Ref:http://www.runoob.com/xpath/xpath-examples.html
		https://segmentfault.com/q/1010000004879947（子节点处理）
	State：
	Date:2017/5/15
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
from lxml import etree


'''
	xpath语法处理器
'''
class CXPath():
	def __init__(self):
		self.url='http://list.v.xunlei.com/v,type/5,movie/page2/'
		self.file='xpath-sample.html'

	def xrespone(self):
		response=urllib2.urlopen(self.url)
		html=response.read()#.decode('utf8')
		seletor=etree.HTML(html)
		links=seletor.xpath('//*[@id="content"]/p[2]/a')
		print links

	def xfile(self):
		selector=etree.HTML(open(self.file,'r').read())
		reslist=selector.xpath('//*[@id="wrapper"]/div[3]/p//text()')
		print reslist
		restext=''.join(reslist).strip()
		print restext.replace(' ','')

		# xpath的string函数的使用
		property_list_reg = '//ul[@id="parameter2"]//li'
		property_lst = selector.xpath(property_list_reg)
		for e in property_lst:
			print(e.xpath('string(.)'))
		#print(len(property_lst))


# 测试入口
if __name__ == "__main__":
	mxpath=CXPath()
	mxpath.xfile()

