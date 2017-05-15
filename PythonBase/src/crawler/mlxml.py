#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:
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

def mlxml():
	url='http://www.runoob.com/xpath/xpath-tutorial.html'
	response=urllib2.urlopen(url)
	html=response.read()#.decode('utf8')
	seletor=etree.HTML(html)
	links=seletor.xpath('//*[@id="content"]/p[2]/a')
	print links

if __name__ == "__main__":
	mlxml()

