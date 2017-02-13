#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:python实现行转列
	Ref:
	State：
	Date:2017/2/13
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')



'''
	需求说明：

	原始数据格式：
	20160215        201607  Mon     43849688
	20160216        201607  Tue     44276770
	20160217        201607  Wed     44819289
	20160219        201607  Fri     44190928
	20160221        201607  Sun     46551557

	目标数据格式：
	周别		Mon Tue Wed Thu Fri Sat Sun
	201607	xx	xx	xx	xx	xx	xx	xx
	201608	xx	xx	xx	xx	xx	xx	xx

'''
from collections import OrderedDict


#vvdict=OrderedDict({"Mon":0,"Tue":0,"Wed":0,"Thu":0,"Fri":0,"Sat":0,"Sun":0}) 使用这种方式不能保证有序
vvdict=OrderedDict([("Mon",0),("Tue",0),("Wed",0),("Thu",0),("Fri",0),("Sat",0),("Sun",0)])

datadict={}
def row2col():
	with open(u'E:\\XMP\\Record\\Problems\\xmp数据预测\local_vod_year_v2','r') as f:
		for line in f:
			date,week,weekday,vv=line.strip().split('\t')
			vvdict[weekday]=vv
			if week not in datadict and week=="Sun":  #每周一清空下字典
				datadict[week]=vvdict
				vvdict.clear()

			print vvdict

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

if __name__ == "__main__":
	row2col()

