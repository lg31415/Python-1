#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:全局判断库
	Ref:
	State：
	Date:2017/7/1
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


####################### eff ##############################
def is_cookieid_eff(cookieid):
	'''
	32位16进制字符串
	'''
	return re.match("^[A-Fa-f0-9]{32}$",cookieid) is not None
def is_peerid_eff(peerid):
	'''
	16位
	'''
	return re.match("^[0-9a-za-Z]{16}$",peerid) is not None
def is_cid_eff(cid):
	'''
	40位16进制字符串
	'''
	return re.match("^[0-9a-fa-F]{40}$",cid) is not None

###################### lang judge ########################
def is_cn_char(i):
	return 0x4e00<=ord(i)<0x9fa6

def is_cn_or_en(i):
	o = ord(i)
	return o<128 or 0x4e00<=o<0x9fa6

def isxdigit(s):
	return re.match(r'^[A-Fa-f0-9]{1,}$',s) is not None

def isJapan(s):
	#return re.search(ur"[\u3040-\u309f]+",unicode(s,"utf-8",'ignore')) is not None or re.search(ur"[\u30a0-\u30ff]+",unicode(s,"utf-8",'ignore')) is not None
	return re.search(ur"[\u3040-\u309f]+",s) is not None or re.search(ur'[\u30a0-\u30ff]+',s) is not None


################### list judge ##########################
from collections import Counter
def listeuql(la,lb,cmpmuti=False,cmporder=False):
	def lcfun(l):
		lc=Counter()
		for i in l:
			lc[i]+=1
		return lc
	if not cmpmuti and not cmporder:
		cmpres=set(la)-set(lb)
		return True if len(cmpres)==0 else False

	if cmpmuti and not cmporder:
		lad=lcfun(la)
		lab=lcfun(lb)
		print lad,lab
		return True if cmp(lad,lab)==0 else False

	if cmpmuti and cmporder:
		return True if cmp(la,lb)==0 else False

	if not cmpmuti and cmporder:
		pass

# 测试入口
if __name__ == "__main__":
    print "相等" if listeuql(list('abcdabcd'),list('dbcadbca'),cmpmuti=True,cmporder=True) else "不相等"

