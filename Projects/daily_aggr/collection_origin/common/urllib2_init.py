# -*- coding: utf-8 -*-
'''
    Fun:urllib2的opener对象cookie初始化
    Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
    State：
    Date:2017/4/28
    Author:tuling56
'''

import os,sys
import hues
import json
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import cookielib


'''
   爬虫urllib2库初始化（cookie方案）
'''
class RequestsBase(object):
    def __init__(self):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'labs')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.opener.close()  #关闭会话

    def htmlfilter(self,tagstring):
        p = re.compile(r'<[^>]+>')
        filtertag = p.sub("", tagstring)
        return filtertag

    # urllib2_cookie的方法有问题(需要将firefox导出的cookie进行转换)
    def init_urllib2_cookie(self,cookie_file=''):
        hues.info("cookie初始化opener对象")
        try:
            cookie = cookielib.MozillaCookieJar(cookies_file)
            handler = urllib2.HTTPCookieProcessor(cookie)
            self.opener = urllib2.build_opener(handler)
            urllib2.install_opener(self.opener)
        except Exception,e:
            hues.error("urllib2加载cookie失败:",str(e))
