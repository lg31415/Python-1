#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:python实现groupby功能
	Ref:
	State：
	Date:2017/6/28
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

class PStat():
	def __init__(self):
		self.src_data='./groupby_data'
		self.posnum={}

	def groupby_sum(self):
		 with open(self.src_data,'r') as f:
			for line in f:
				try:
					pos,pv,uv=line.strip('\n').split()  #按第一列分组，对第二，三列就行汇总
				except Exception,e:
					print str(e),line
					continue

				if self.posnum.has_key(pos):
					self.posnum[pos][1]+=int(pv)
					self.posnum[pos][2]+=int(uv)
				else:
					if pos=='movie':
						self.posnum[pos]=[1,int(pv),int(uv)]
					elif pos=='teleplay':
						self.posnum[pos]=[2,int(pv),int(uv)]
					elif pos=='tv':
						self.posnum[pos]=[3,int(pv),int(uv)]
					elif pos=='anime':
						self.posnum[pos]=[4,int(pv),int(uv)]
					elif pos=='vmovie':
						self.posnum[pos]=[5,int(pv),int(uv)]
					elif pos=='joke':
						self.posnum[pos]=[6,int(pv),int(uv)]
					elif pos=='mvzhibo': #(jiuwo)
						self.posnum[pos]=[7,int(pv),int(uv)]
					elif pos=='zhibo':
						self.posnum[pos]=[8,int(pv),int(uv)]
					elif pos=='documentary':
						self.posnum[pos]=[9,int(pv),int(uv)]
					elif pos=='femalestars':
						self.posnum[pos]=[10,int(pv),int(uv)]
					else: #unknown
						self.posnum[pos]=[-1,int(pv),int(uv)]
		 print self.posnum


# 测试入口
if __name__ == "__main__":
    pstat=PStat()
    pstat.groupby_sum()

