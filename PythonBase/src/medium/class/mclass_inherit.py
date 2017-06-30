#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:类继承演示
	Ref:
	State：
	Date:2017/6/29
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


class CBase():
	def __init__(self):
		print '基类构造'
		self.base_var1="基类公共变量"
		self._base_priv_var1="_基类私有变量"
		self.__base_priv_var1="__基类私有变量"
	def __del__(self):
		print '基类析构'
	def base_pubm_1(self):
		print "基类公共方法1"
	def _base_prim_1(self):
		print "_基类私有方法1"
	def __base_prim_1(self):
		print "__基类私有方法1"

class CSub(CBase):
	sub_var1="这是子类的类变量"
	#def __init__(self):
	#	print '子类构造'
	def __del__(self):
		print '子类析构'
	def pubm_1(self):
		print "子类公共方法1"
	def _prim_1(self):
		print "_子类私有方法1"
	def __prim_1(self):
		print "__子类私有方法1"

	# 子类调用基类公共函数
	def subinvokebase(self):
		self.base_pubm_1()
		print self.base_var1
		print self.sub_var1
		print self._base_priv_var1

# 测试入口
if __name__ == "__main__":
	cs=CSub()
	cs.subinvokebase()

