#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:trie树的字典实现
	Ref:
	State：
	Date:2017/6/6
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


class Trie():
	root={}
	END='/'
	def __init__(self):
		print '----init------'

	def add(self,word):
		node=self.root
		for c in word:
			node.setdefault(c,[]).append(c)
			node=node.get(c) # 返回的是list
		node[self.END]=None


	def search(self,word):
		node=self.root
		for c in word:
			if c not in node:
				return False
			node=node[c]
		return self.END in node

	def __del__(self):
		print '-----delete-------'

# 测试入口
if __name__ == "__main__":
	mt=Trie()
	mt.add('china')
	mt.add('america')
	print mt.root
