#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：自动订餐系统（cookie的获取保存和使用）
  参考：http://python.jobbole.com/81344/
'''
import urllib
import urllib2
import cookielib
import json
import re
from bs4 import BeautifulSoup

'''
    cookie公共类
'''
class mCookie():
    def __init__(self):
        self.visurlurl="http://192.168.16.33/meal/" #'http://192.168.16.33/meal/'   #访问网址
        self.filename='cookie.txt'   #保存cookie的文件

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
        #解析cookie内容
        for item in cookie:
            print "Domain:"+item.domain+"\tPath:"+item.path+"\tName="+item.name+"\tValue="+item.value
        #保存cookie到文件
        cookie.save(ignore_discard=True, ignore_expires=True)

    # 先用密码登录并保存cookie，再使用cookie访问
    def requestWithCookie(self):
        #保存登录cookie
        filename='logincookie'
        loginurl = 'http://home.xunlei.com/plaf/login.jsf'
        postdata=urllib.urlencode({
            'username':'yuanjunmiao',
            'password':'2Jzn2Q7ue49W', #'42852644fea1cb03f80b1a700368047f%26%23646215'
            'lt':'e4s1',
            'eventId':'submit',
            'cookie':-1
        })
        cookie=cookielib.MozillaCookieJar(self.filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        respone = opener.open(loginurl, postdata)
        cookie.save(ignore_discard=False,ignore_expires=False)
        #用登录cookie模拟登录
        result=opener.open(self.visurlurl)
        print result.read()

    # 使用豆瓣测试通过
    def doubantest(self):
        #保存登录cookie
        filename='logincookie'
        loginurl = 'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001'
        postdata=urllib.urlencode({
            'username':'yueqiulaishu@163.com',
            'password':'a112233'
        })
        cookie=cookielib.MozillaCookieJar(filename)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        respone = opener.open(loginurl, postdata)
        cookie.save(ignore_discard=False,ignore_expires=False)
        #用登录cookie模拟登录
        visiturl="https://www.douban.com/people/45545682/"
        result=opener.open(visiturl)
        print result.read()



    # 字符串hex化
    def str2hex(self,cstr):
        hexs=cstr.encode('hex')
        hexss=[hexs[x:x+2] for x in range(0,len(hexs),2)]
        hexstr='%'+'%'.join(hexss)
        return  hexstr

    def uridecode(self,uristr):
        pass



'''
    订餐类
'''
class mDinner(mCookie):
    def __init__(self):
        mCookie.__init__(self)

    #构造header头
    def buildHead(self):
        pass

    #获取菜单
    def getMenu(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
            "cookie": "JSESSIONID=33D152C30873FFEF8BD2A15B4C8D8370; xl_meal_area=20140307-8b1521eb656044eba47107de5002927c;base_auth_code=529481d1adb127bbad7002efcd80913a824057; base_sid=abafaf516c7d4174acef481696212b15; xl_menu_uuid=f06df1133a984747af4cd83ce9b66bbf; xl_menu_name=%E5%B0%8F%E7%82%92%E8%8C%84%E5%AD%90; xl_menu_rest=%E5%A4%A9%E5%BA%9C%E5%B7%9D%E9%A6%99%0A"
        }
        request=urllib2.Request(self.url,None,headers)
        print self.url
        response=urllib2.urlopen(request)
        html=response.read().decode('utf8')
        soup=BeautifulSoup(html)
        print soup
        resturants=soup.find('section',id='rest_cell0')
        print resturants
        #all=soup.findAll('li')
        #print all

    #订餐
    def loginwithcookie(self):
        rest=['天府川香','美味通']
        hexrest=map(self.str2hex,rest)
        headers = {
                "Host": "192.168.16.33",
                "Referer": "http://192.168.16.33/meal/",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
                "cookie": "JSESSIONID=92969F46F27FF34CC44854179AB0C2CE; base_auth_code=238826905dd109a75a9bad72d7147d5a87f66e; base_sid=767f478cc0094361868d921c54aef240; xl_meal_area=20140307-8b1521eb656044eba47107de5002927c; xl_menu_uuid=78f5de0de31841d5ac2ea3fe1a665cfa; xl_menu_name=%E5%9C%9F%E8%B1%86%E7%89%87%E5%8D%A4%E7%89%9B%E8%82%89; xl_menu_rest=%E5%A4%A9%E5%BA%9C%E5%B7%9D%E9%A6%99%0A"
            }
        postdata=urllib.urlencode({
                    'menu_uuid':'78f5de0de31841d5ac2ea3fe1a665cfa',   #需要上报的关键信息
                    'area_uuid':'20140307-8b1521eb656044eba47107de5002927c'
                }
            )
        request=urllib2.Request("http://192.168.16.33/meal/spmvc/user_submit_order",None,headers)
        resonse=urllib2.urlopen(request,postdata)
        content=resonse.read().decode('utf8')
        pdict=json.loads(content)
        print pdict
        f=open('orderres','w')
        json.dump(pdict,f)
        f.close()


if __name__ == "__main__":
    mcookie=mCookie()
    mcookie.requestWithCookie()
    #mcookie.savecookie()
    #mcookie.doubantest()
    #mcookie.loginwithcookie()
    exit()

    mdinner=mDinner()
    mdinner.getMenu()
