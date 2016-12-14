#!/usr/bin/env python
#-*-coding:utf8-*-
__author__ = 'yjm'
'''
  功能注释：播放排行统计
'''

#import MySQLdb
import json
import urllib2
import os
import sys
#import commands
import re
#from datetime import date, datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf8')

#获取url
def getUrl(cid,filesize):
    if len(cid)!=40:
        print "\033[31m Wrong cid: %s\033[0m" %cid
        exit()
    wwwroot="http://hotview.v.xunlei.com"
    first_p=cid[0:2]
    second_p=cid[2:4]

    # filesize="查询mysql获得"
    filename=cid+'.'+filesize
    url=os.path.join(wwwroot,first_p,second_p,filename)
    return url

# 利用urllib2库得到内容并完成历史数据备份（已完成）
url="http://hotview.v.xunlei.com/8E/F0/8EF06B4F43F6EF9CB6F4B8C2DF06CB9555C7120F.1324471559"
def getUrlContent(url):
    # 路径获取(将数据备份到rootpath根目录下)
    rootpath=""
    lpath=re.split(re.compile('/{1,2}'),url)
    (firstl_path,secondl_path,filename)=lpath[2:5]
    cidfilesize=re.split('\.',filename)
    if len(cidfilesize)==2:
        cid=cidfilesize[0]
        filesize=cidfilesize[1]
        datapath=os.path.join(rootpath,firstl_path,secondl_path)
        datafile=os.path.join(rootpath,firstl_path,secondl_path,filename)
        if not os.path.exists(datapath):
            os.mkdir(datapath)
    else:
        print "\033[31m Wrong split:%s\033[0m" %url
        exit()

    # 文件内容备份（才用追加的方式）
    fdata=open(datafile,'a+')
    resonse=urllib2.urlopen(url)
    content=resonse.read().decode('utf8')
    plist=json.loads(content) 	# 解析后得到的字典，字典的值是热力图的数据
    if plist.get('hot_view'):
        hotdata=plist['hot_view']
        fdata.write('\t'.join(map(str,hotdata)))
        fdata.write('\n')
    fdata.close()


if  __name__=="__main__":
    getUrlContent(url)
