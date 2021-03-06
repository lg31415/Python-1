#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：cookie的获取保存和使用
  参考：http://python.jobbole.com/81344/
'''

import sys
import json
import re
import urllib
import urllib2
import cookielib
import hues
from bs4 import BeautifulSoup
from collections import OrderedDict

reload(sys)
sys.setdefaultencoding('utf-8')

'''
    cookie公共类
'''
class mCookie():
    def __init__(self):
        self.url="https://wz.cnblogs.com/"
        self.filename='mcookie.log'

    # 保存网页
    def savehtml(self,content):
        with open('mcookie.html','w') as f:
            f.write(content)

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
        self.savehtml(response.read().decode('utf-8').encode('utf-8'))

        #解析cookie内容（可能保存的是很多的cookie）
        for item in cookie:
            print "Domain:"+item.domain+"\tPath:"+item.path+"\tName="+item.name+"\tValue="+item.value

        #保存cookie到文件
        cookie.save(ignore_discard=True, ignore_expires=True)

    # 先用密码登录并保存cookie，再使用cookie访问
    def requestWithCookie(self):
        # 登录并保存cookie
        loginurl = 'https://passport.cnblogs.com/user/signin'
        postdata=urllib.urlencode({
            'username':'yuanjunmiao',
            'password':'2Jzn2Q7ue49W'
        })
        cookie=cookielib.MozillaCookieJar('logincookie.log')
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        response = opener.open('https://wz.cnblogs.com/', postdata)
        cookie.save(ignore_discard=False,ignore_expires=False)

        # 用登录cookie模拟登录
        result=opener.open(self.url)  #这个时候带cookie了吗???
        print result.read()

    # 字符串hex化
    def __str2hex(self,cstr):
        hexs=cstr.encode('hex')
        hexss=[hexs[x:x+2] for x in range(0,len(hexs),2)]
        hexstr='%'+'%'.join(hexss)
        return  hexstr


'''
    cookie加载和转换
'''
class LoadCookie():
    def __init__(self):
        self.cookies=[]

    #加载chrome的edit_this_cookie导出的cookie
    def load_chrome_cookie(self):
        with open('chrome_cookies.ck','r') as f:
            try:
                chrome_cookies=json.load(f,encoding='utf-8')#,object_pairs_hook=OrderedDict)
                for ck in chrome_cookies:
                    self.cookies.append({'name':ck['name'],'value':ck['value']})
                print self.cookies
            except Exception,e:
                hues.error('解析chrome_cookies失败:',str(e))

    # 加载firefox的firedebug导出的cookie
    def load_firefox_cookie(self):
        with open('firefox_cookies.ck','r') as f:
            try:
                for line in f:
                    name,value=line.strip().strip('\n').split('\t')[-2:]
                    self.cookies.append({'name':name,'value':value})
                print self.cookies
            except Exception,e:
                hues.error('解析firefox_cookies失败:',str(e))

    # 加载cookielib保存的cookie
    def load_morzila_cookie(self):
        with open('morzila_cookies.ck','r') as f:
            try:
                for line in f:
                    line=line.strip().strip('\n').decode('ascii').encode('utf8')
                    if line.startswith('#') or line=='':
                        continue
                    name,value=line.split('\t')[-2:]
                    self.cookies.append({'name':name,'value':value})
                print self.cookies
            except Exception,e:
                hues.error('解析morzila_cookies失败:',str(e))




# 测试入口
if __name__ == "__main__":
    #mcookie=mCookie()
    #mcookie.savecookie()
    #mcookie.requestWithCookie()

    lc=LoadCookie()
    lc.load_chrome_cookie()
    #lc.load_firefox_cookie()
    #lc.load_morzila_cookie()

