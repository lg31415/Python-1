#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：下载和保存固定网址的mp3视频,主要是urlib2库的使用
'''

import re
import urllib,urllib2

'''
    首先获取全部的url
'''
entry_url="http://www.tingshuge.com/Book/2379.html"
def getAllURL_api(entry_url):
    regex=re.compile(r'/down/\?2379-\d{1,3}\.html')
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    headers = {'User-Agent' : user_agent}
    request = urllib2.Request(entry_url,None,headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError,e:
        print e.reason
    content= response.read().decode('gbk')
    resl=re.findall(regex,content)
    return  resl

'''
    对每个url进行处理
'''
def getMp3_api(iurl):
    url = "http://www.tingshuge.com"+iurl;
    numr=re.search(r'(?<=-)\d{1,3}(?=\.html)',iurl)
    if numr:
        num=int(numr.group())+1
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    headers = {'User-Agent' : user_agent}
    request = urllib2.Request(url,None,headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError,e:
        print e.reason
    page = response.read().decode('gbk')
    pattern = re.compile(r"http://audio\.kting\.cn/Other/Sample_Audio.*\.mp3")
    rest=re.search(pattern,page)
    if rest:
        bytes1=urllib2.urlopen(rest.group())
        f = open("D://"+str(num)+".mp3", 'wb');
        f.write(bytes1.read());   #利用url打开音频的地址，然后二进制写入
        f.flush();
        f.close();

'''
    入口：下载音频
'''
def down_mp3_entry():
    allurl=getAllURL_api(entry_url)
    for url in allurl:
        getMp3_api(url)


'''
    构造post请求(在请求的时候传送body体)
'''
from collections import OrderedDict
def buildpost():
    data={'username':'zawe','password':'12342'}
    data={'u':'mediaso','u1':'click','u2':'search','u3':'thisu3','u4':'AWFEWKEDWDWDWEWLDW','u5':'jjwewew','rd':12243543544}
    data=OrderedDict([('u','mediaso'),('u1','click'),('u2','search'),('u3','thisu3'),('u4','AWFEWKEDWDWDWEWLDW'),('u5','jjwewew'),('rd',12243543544)])
    #posturl='http://kkpgv3.stat.kankan.com/'
    #postdata=urllib.urlencode(data)
    #print postdata
    #req=urllib2.urlopen(posturl,postdata);
    url="http://kkpgv3.stat.kankan.com/?u=mediaso&u1=click&u2=search&u4=XXXFXXXXXXXXXXXE&rd=1470057248"
    req=urllib2.urlopen(url)
    content=req.read()



# 测试
if __name__ == "__main__":
    #down_mp3_entry()
    buildpost()

