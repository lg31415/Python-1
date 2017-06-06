#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:字符串处理实战
	Ref:
	State：
	Date:2017/6/5
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

# 引入字符串处理工具
import string_proc as sp


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

# 字符列表处理
def filter_str_list():
	strlist=['\n                ', u'\u8fd9\u662fspan1', '\n                ', u'\u8fd9\u662fspan2', '\n                8.9\n']
	strlist_filter=filter(lambda x:sp.judge_mean(x),strlist)
	strlist_filter=map(sp.remove_meanless,strlist_filter)
	print strlist_filter


# 测试入口
if __name__ == "__main__":
    filter_str_list()

