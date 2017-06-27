#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:url解析
	Ref:http://blog.csdn.net/haoni123321/article/details/15814111/
	State：初步完成
	Date:2017/4/24
	Author:tuling56
'''
import re, os, sys
import hues
from urllib import quote,unquote
from urllib import urlencode  #注意没有urldecode()这个函数

reload(sys)
sys.setdefaultencoding('utf-8')


'''
	字符串hex化
	输入：中国
	输出：%E4%B8%AD%E5%9B%BD
'''
def str2hex(instr):
	hexs=instr.encode('hex')
	hexss=[hexs[x:x+2] for x in range(0,len(hexs),2)]
	hexstr='%'+'%'.join(hexss)
	print "hex:",hexstr
	return  hexstr

def mquote(instr):
	hexstr=quote(instr)
	print "hex:",hexstr
	return  hexstr


'''
	字符串反hex化
	输入：%E4%B8%AD%E5%9B%BD
	输出：中国
'''
def hex2str(hexstr):
	hexstr=hexstr.replace('%','')
	print "剔除%:",hexstr
	unhexstr=hexstr.decode('hex')
	print "反hex:",unhexstr
	return unhexstr

def munquote(hexstr):
	unhexstr=unquote(hexstr)
	#print "反hex:",unhexstr
	return unhexstr



'''
	url整体编解码
'''

class URLParse():
	def __init__(self):
		self.url="http://48.fans.xunlei.com/catalog/catalog.shtml?team=SNH48&group=SⅡ&member=许佳琪"
		self.url_encode="http%3A%2F%2F48.fans.xunlei.com%2Fcatalog%2Fcatalog.shtml%3Ftype%3D%E9%9F%B3%E4%B9%90%26subtype%3DMV"

	#编码url字符串
	# urlencode函数，把字典对转换所需要的格式
	def murlencode(self):
		data={
			'teamp':'SNH48',
			'group':'SⅡ',
			'member':'许佳琪'
		}
		print urlencode(data)
		#结果：member=%E8%AE%B8%E4%BD%B3%E7%90%AA&group=S%E2%85%A1&teamp=SNH48，注意&符号没有被编码

		#对单个字符进行url编码
		print quote('许佳琪')


	# 解析url字符串（含中文）
	def murldecode(self):
		with open('./data/snh48_click_origin_20170423','r') as f:
			for line in f:
				fu2,fu4=line.strip().split()
				print fu4
				print unquote(fu4)
				print '----------------------------------------------------------'


# 测试入口
if __name__ == "__main__":
	murl=URLParse()
	murl.murlencode()
	murl.murldecode()

