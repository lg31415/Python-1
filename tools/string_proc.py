#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:字符串处理类
	Ref:
	Date:2016/10/19
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


#################### 判断 #################
#判断单个字符是否是中文
def is_cn_char(i):
	return 0x4e00<=ord(i)<0x9fa6

# 判断但字符是否中文或英文
def is_cn_or_en(i):
	o = ord(i)
	return o<128 or 0x4e00<=o<0x9fa6

# 判断字符是否是16进制数
def isxdigit(s):
	return re.match(r'^[A-Fa-f0-9]{1,}$',s) is not None

# 判断字符是否是日文
def isJapan(s):
	'''
	unicode
	'''
	#return re.search(ur"[\u3040-\u309f]+",unicode(s,"utf-8",'ignore')) is not None or re.search(ur"[\u30a0-\u30ff]+",unicode(s,"utf-8",'ignore')) is not None
	return re.search(ur"[\u3040-\u309f]+",s) is not None or re.search(ur'[\u30a0-\u30ff]+',s) is not None


#################### 操作 #################
# 去除标点符号和无效字符
def remove_comm(s):
	patern=re.compile(r'[\r\n\t\s【】;:,：，；*?\]\[]?')
	sr=re.sub(patern,'',ntitle)
	print(sr)
	return sr

# 替换字符（用函数来判断规则）
def resub():
	s = 'i say, hello world!'
	pattern = re.compile(r'(\w+) (\w+)')
	print re.sub(pattern,r'\2 \1', s)

	# 嵌套定义
	def func(m):
		return m.group(1).title() + ' ' + m.group(2).title()

	print re.sub(pattern,func, s)




############## 实战部分 #####################
ntitle="【资源公众号-影视资源狗】【电影-www.】.2016.HD720P.影视资源狗.mp4"
ntitle="zhan\t zhv33 【 zhjang ] * whwr】: ：，;；\r [鸟哥的\n\t"
ntitle=u"[BuRongYi.com]盗墓笔记.HD1280高清国语中英双字.mp4"
ntitle="【欧美短片】（骚女和黑屌14.20分钟）.mp4"


# 字符处理函数
def filter_str():
	global ntitle

	# 去除指定模式
	patern=re.compile(r'【[^】]*电影[^】]*】')    #删除包含电影的
	patern=re.compile(r'【[^】]*www\.[^】]*】')  #删除包含www.的
	patern=re.compile(r'\w{1,}语\w双?字幕?')	    #删除字幕（中文字符的正则匹配问题）

	pps=re.findall(patern,ntitle)
	for pp in pps:
		print "删除:",pp
		ntitle=ntitle.replace(pp,'')

	print "处理后的字符：",ntitle

if __name__ == "__main__":
	filter_str()
	#resub()

