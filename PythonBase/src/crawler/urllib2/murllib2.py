#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
    功能：urllib2库的使用
    ref:http://blog.chinaunix.net/uid-12014716-id-5763287.html  # 超时问题
        http://www.cnblogs.com/sysu-blackbear/p/3629770.html
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
            print "超时，可能需要重试",str(e)

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



# 测试入口
if __name__ == "__main__":
    mb=BaseUrlib2()
    mb.url_post()


