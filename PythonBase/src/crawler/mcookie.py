#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：cookie的获取保存和使用
  参考：http://python.jobbole.com/81344/
'''

import json
import re
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

'''
    cookie公共类
'''
class mCookie():
    def __init__(self):
        self.url="http://sso.sandai.net/server/login?service=http://192.168.16.33/meal/" #'http://192.168.16.33/meal/'
        self.filename='cookie.txt'

    # 访问并保存cookie
    def savecookie(self):
        #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
        cookie = cookielib.MozillaCookieJar(self.filename)
        #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        handler = urllib2.HTTPCookieProcessor(cookie)
        #通过handler来构建opener
        opener = urllib2.build_opener(handler)
        #创建一个请求，原理同urllib2的urlopen
        response = opener.open(self.url)

        #解析cookie内容（可能保存的是很多的cookie）
        for item in cookie:
            print "Domain:"+item.domain+"\tPath:"+item.path+"\tName="+item.name+"\tValue="+item.value

        #保存cookie到文件
        cookie.save(ignore_discard=True, ignore_expires=True)

    # 先用密码登录并保存cookie，再使用cookie访问
    def requestWithCookie(self):
        # 登录并保存cookie
        filename='logincookie'
        loginurl = 'http://sso.sandai.net/server/login?service=http://192.168.16.33/meal/'
        postdata=urllib.urlencode({
            'username':'yuanjunmiao',
            'password':'2Jzn2Q7ue49W'
        })
        cookie=cookielib.MozillaCookieJar(filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        respone = opener.open(loginurl, postdata)
        cookie.save(ignore_discard=False,ignore_expires=False)

        # 用登录cookie模拟登录
        result=opener.open(self.url)  #这个时候带cookie了吗???
        print result.read()




# 测试入口
if __name__ == "__main__":
    mcookie=mCookie()
    #mcookie.savecookie()
    mcookie.requestWithCookie()
    #mcookie.loginwithcookie()

