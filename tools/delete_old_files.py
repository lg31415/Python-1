#!/usr/bin/env python
# -*- coding: utf8 -*-
#add by maohaibo@xunlei.com 20150702

import os
import sys
import time
from datetime import date,  datetime, timedelta

########################################
#获取中间文件路径
########################################
file_path=os.getcwd()
file_path=file_path.replace("/bin","/data")

########################################
#获取文件列表
########################################
file_list = []
for filename in os.listdir(file_path):
    if filename.endswith(".txt"):
        file_list.append(filename)

#print file_list


## 计算过期日期
today=time.strftime('%Y%m%d',time.localtime(time.time()))
end_day=date(int(today[0:4]),int(today[4:6]),int(today[-2:]))-timedelta(days=30)

for file in file_list:
	t=os.stat(file)[8]
	file_mdate=time.strftime('%Y%m%d',time.localtime(t))
	#print file, file_mdate
	fmd='%04d%02d%02d' %(end_day.year, end_day.month, end_day.day)
	#print fmd
	if file_mdate < fmd:
		os.remove(file)
		print "file %s has deleted!!!" % file



