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
import json

reload(sys)
sys.setdefaultencoding('utf-8')

'''
	单字符判断
'''
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


'''
	字符串操作
'''
# 去除标点符号和无效字符
def remove_meanless(instr):
	patern=re.compile(r'[\r\n\t\s【】;:,：，；*?\]\[]?')
	sr=re.sub(patern,'',instr)
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

# 判断字符串是否是有意义串
def judge_mean(instr):
	sr=remove_meanless(instr)
	if len(sr)==0:
		return False
	else:
		return True


# 字符串转字典
def str_to_dict():
	instr='name=zhang&age=12'
	d=dict(map(lambda x:x.split('='),instr.split('&')))
	dstr=str(d)
	dstr_json=dstr.replace('\'','"')

	print d
	print dstr
	print dstr_json	 #json解析的字符串必须是双引号括住的

	print json.loads(dstr_json)#,encoding='utf8')






# 测试入口
if __name__ == "__main__":
	#filter_str()
	#judge_mean()
	str_to_dict()


