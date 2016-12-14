#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Date:
	Author:tuling56
	Fun:
'''
import os
import sys
import time
from datetime import date, datetime, timedelta

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

# 日期参数处理
if len(sys.argv) <= 1:
	yesterday = date.today() - timedelta(days=1)
	yesterday = yesterday.strftime("%Y%m%d")
else:
	yesterday = sys.argv[1]


class MediaInfo(object):
    def __init__(self,name): 
        self.name=name
  
    def getTypeTitle(movieid):
		url='http://media.v.xunlei.com/pc/info?movieid='+movieid
		headers ={
			"Host":"media.v.xunlei.com",
			"Referer": "http://media.v.xunlei.com",
			"cookie":"client=pc;version=5.1.0.3054"
		}
		request=urllib2.Request(url,None,headers)
		resonse=urllib2.urlopen(request)
		content=resonse.read().decode('utf8')
		pdict=json.loads(content) #解析后得到的字典
		mtype=pdict.get('type','Unknown')
		mtitle=pdict.get('title','Unknown')
		return mtype,mtitle
	

'''
	主入口
'''
if __name__ == "__main__":
	# 实例方法
    # myc=CTest('hahha') ;
    # myc.instanceMethod()#myc.printstr(); #等同于调用Test.printstr(myc)printstr在定义时没有参数，在调用的时候传递了参数
    # CTest.classMethod()    #在调用的时候也不传类实例，但提示错误
	print "main"

