#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:cookie的验证和使用
	Ref:
	State：
	Date:2017/8/23
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import json
import re
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup


'''
    cookie的验证和使用
'''
class CookieApplication():
    def __init__(self):
        pass

    # 豆瓣测试：冏的是要访问的页面不用使用cookie验证登录就可以看的
    def doubanloigin(self):
        #保存登录cookie
        filename='douban_cookie.txt'
        loginurl = 'https://www.douban.com/accounts/login?source=main'
        postdata=urllib.urlencode({
            'username':'yueqiulaishu@163.com',
            'password':'avvvv'
        })
        cookie=cookielib.MozillaCookieJar(filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        opener.open(loginurl, postdata)
        cookie.save(ignore_discard=False,ignore_expires=False)

        #用登录cookie模拟登录
        visiturl="https://www.douban.com/people/45545682/"
        result=opener.open(visiturl)
        print result.read()

    # 豆瓣cookie测试(成功,cookie是事先导出保存的)
    def douban(self):
        #创建MozillaCookieJar实例对象
        cookie = cookielib.MozillaCookieJar()
        #从文件中读取cookie内容到变量
        cookie.load('douban_cookies_mod.txt', ignore_discard=True, ignore_expires=True)
        #创建请求的request
        req = urllib2.Request("https://www.douban.com/accounts/")
        #利用urllib2的build_opener方法创建一个opener
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        response = opener.open(req)
        print response.read()


    # 博客园cookie测试(成功,cookie是事先导出保存的)
    def cnblog(self):
        #创建MozillaCookieJar实例对象
        cookie = cookielib.MozillaCookieJar()
        #从文件中读取cookie内容到变量
        cookie.load('cnblog_cookies.txt', ignore_discard=True, ignore_expires=True)
        #创建请求的request
        req = urllib2.Request("https://wz.cnblogs.com/")
        #利用urllib2的build_opener方法创建一个opener
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        response = opener.open(req)
        print response.read()


# 测试入口
if __name__ == "__main__":
    ca=CookieApplication()
    ca.douban()
    #ca.cnblog()

