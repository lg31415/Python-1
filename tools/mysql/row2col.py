#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:python实现行转列
	Ref:http://blog.csdn.net/jackfrued/article/details/45021897?ref=myread
	State：开发中
	Date:2017/2/13
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

'''
	基本的行列转换
	ref:http://outofmemory.cn/code-snippet/6182/python-form-row-column-together-switch
	imp:如何笔记两个列表是否相等
'''
def basic_row2col():
	# 行数据（每一行代表一条记录）
	row=[('Person', 'Disks', 'Books'),
		 ('Zoe', 12, 24),
		 ('John', 17, 5),
		 ('Julien', 3, 11)]

	# 列数据（每一列代表一条记录）
	col=[('Person', 'Zoe', 'John', 'Julien'),
		 ('Disks', 12, 17, 3),
		 ('Books', 24, 5, 11)]

	if col==zip(*row):
		print u'行-->列 成功'
	else:
		print u'行-->列 失败！'

	if row==zip(*col):
		print u'列-->行 成功'
	else:
		print u'列-->行 失败！'




'''
	实战应用
	行转列（长格式转宽格式）

	需求说明：
	（注意剔除了日期这列的数据）

	原始数据格式（行式）：
	20160214		201606	Sun		46334034
	20160215        201607  Mon     43849688
	20160216        201607  Tue     44276770
	20160217        201607  Wed     44819289
	20160219        201607  Fri     44190928
	20160221        201607  Sun     46551557

	目标数据格式（列式）：
	周别		Mon Tue Wed Thu Fri Sat Sun
	201607	xx	xx	xx	xx	xx	xx	xx
	201608	xx	xx	xx	xx	xx	xx	xx

'''
from collections import OrderedDict

#vvdict=OrderedDict({"Mon":0,"Tue":0,"Wed":0,"Thu":0,"Fri":0,"Sat":0,"Sun":0}) 使用这种方式不能保证key有序
vvdict=OrderedDict([("Mon",-1),("Tue",-1),("Wed",-1),("Thu",-1),("Fri",-1),("Sat",-1),("Sun",-1)])

# 辅助函数：重置字典的默认值
def reset_dict():
	for k in vvdict.keys():
		vvdict[k]=-1

# 辅助函数：转换后的信息导出
def export_result():
	# 打印头
	for key in vvdict.keys():
		print key+"\t",
	print

	# 打印内容
	for k,v in datadict.iteritems():
		print k,
		for ww,vv in v.iteritems():
			print vv,
		print



# 实现函数：行转列的终极实现
def application_row2col():
	datadict={}  # 最终的数据结构字典
	# method1
	'''
	with open(u'row2col.data', 'r') as f:
		weekstart,weekend=True,False
		for line in f:
			week,weekday,vv=line.strip().split('\t')
			vvdict[weekday]=vv
			if week not in datadict.keys() or not datadict: # 字典为空或者该周别不在字典中
				if not weekstart:
					datadict[week]='\t'.join([str(v) for v in vvdict.values()])
					reset_dict()
				else:
					print u'该周还在继续'
			else:
				weekstart=False
				weekend=False
	print datadict
	sys.exit()
	'''

	# method2
	with open(u'row2col.data', 'r') as f:
		preweek=''
		weekstart=True
		week_end=False
		for line in f:
			week,weekday,vv=line.strip().split('\t')
			vvdict[weekday]=vv
			if week!=preweek:
				weekstart=True
				preweek=week
			else:
				weekstart=False  # 该州的数据在继续



			#这是更新
			datadict[preweek]='\t'.join([str(v) for v in vvdict.values()]) # 更新


# 测试入口
if __name__ == "__main__":
	#basic_row2col()
	application_row2col()


