#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
    功能：urllib2库的使用
    ref:http://blog.chinaunix.net/uid-12014716-id-5763287.html  # 超时问题
    state:
'''

import re
import urllib,urllib2
import json
from collections import OrderedDict

import socket
socket.setdefaulttimeout(60)    # 设置全局socket超时时间60s


'''
    基本使用
'''
class BaseUrlib2():
    def __init__(self):
        pass

    #构造post请求(在请求的时候传送body体)
    def url_post(self):
        data={'username':'zawe','password':'12342'}
        data={'u':'mediaso','u1':'click','u2':'search','u3':'thisu3','u4':'AWFEWKEDWDWDWEWLDW','u5':'jjwewew','rd':12243543544}
        data=OrderedDict([('u','mediaso'),('u1','click'),('u2','search'),('u3','thisu3'),('u4','AWFEWKEDWDWDWEWLDW'),('u5','jjwewew'),('rd',12243543544)])
        posturl='http://kkpgv3.stat.kankan.com/'
        postdata=urllib.urlencode(data)   # 注意编码方式
        print "编码后的post数据：",postdata
        req=urllib2.urlopen(posturl,postdata,timeout=20)
        try:
            content=req.read()
            print content.req.url
        except Exception,e:
            print "超时，可能需要重试"

    # 构造get请（不带header头）
    def url_get(self):
        url="http://kkpgv3.stat.kankan.com/?u=mediaso&u1=click&u2=search&u4=XXXFXXXXXXXXXXXE&rd=1470057248"
        req=urllib2.urlopen(url,timeout=20)
        content=req.read()
        print content

    # 演示完整使用
    def demo(self,base_url, query=""):
        req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded'}
        req_timeout = 3    #使用urllib2库本身自带的超时参数，一般情况下接口设置为3s，网页抓取设置为5s
        url = ""
        if query:
            url = base_url + "&kw=" + urllib2.quote(query)
        else:
            url = base_url
        print url
        req = urllib2.Request(url, None, req_header)
        # print req
        retryTime = 3
        return_dict = {}
        while retryTime > 0:
            try:
                doc = urllib2.urlopen(req, None, timeout=req_timeout).read()
                return json.loads(doc)
            except Exception, e:
                if retryTime == 1:
                    # logger.error(str(e)+', url:'+url)


                    print 'reTryTime:',retryTime,'\n\n'
                    retryTime -= 1
        return return_dict

'''
    应用1：获取和下载MP3
    功能注释：下载和保存固定网址的mp3视频,主要是urlib2库的使用
'''
class ExDownMP3():
    def __init__(self):
        self.entry_url="http://www.tingshuge.com/Book/2379.html"

    # 首先获取全部的url（带header头）
    def getAllURL_api(self):
        regex=re.compile(r'/down/\?2379-\d{1,3}\.html')
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
        headers = {'User-Agent' : user_agent}
        request = urllib2.Request(self.entry_url,None,headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError,e:
            print e.reason
        content= response.read().decode('gbk')
        resl=re.findall(regex,content)
        return  resl

    # 对每个url进行处理
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
            f.write(bytes1.read())      # 利用url打开音频的地址，然后二进制写入
            f.flush()
            f.close()

    #入口：下载音频
    def down_mp3_entry(self):
        allurl=self.getAllURL_api(self.entry_url)
        for url in allurl:
            self.getMp3_api(url)


# 测试入口
if __name__ == "__main__":
    mb=BaseUrlib2()
    mb.url_post()

