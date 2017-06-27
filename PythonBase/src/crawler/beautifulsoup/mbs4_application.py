#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:
	State：
	Date:2017/6/23
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import urllib
import socket
from bs4 import BeautifulSoup    #html
from bs4 import BeautifulStoneSoup  #xml
from bs4 import Tag,NavigableString

'''
    BS4应用
'''
class mBS4Ex():
    def __init__(self):
        pass
    '''
       下载网页中符合条件的js脚本
    '''
    def getjs(self):
        url='http://toutiao.com/a6319057072252420354/'
        response=urllib2.urlopen(url)
        html=response.read().decode('utf8')
        soup=BeautifulSoup(html)
        jss=soup.findAll('script',{'type':'text/javascript'})
        jssurls=[]
        for js in jss:
            jsurl=js.get('src')
            if not jsurl:
                continue
            if re.match(re.compile(r'//'),jsurl):
                jsurl='http:'+jsurl
            jssurls.append(jsurl)

        for jsurl in jssurls:
            print jsurl
            filename=os.path.split(jsurl)[1]
            urllib.urlretrieve(jsurl,filename)

    '''
      遍历和下载图像
    '''
    def getpic(self):
        url='http://toutiao.com/a6319057072252420354/'
        response=urllib2.urlopen(url)
        html=response.read().decode('utf8')
        soup=BeautifulSoup(html)
        article=soup.find('div',{'class':'article-content'})
        imgs=article.findAll('img')
        imgurls=[]
        for img in imgs:
            imgurl=img.get('src')
            imgurls.append(imgurl)

        for imgurl in imgurls:
            print imgurl
            filename=os.path.split(imgurl)[1]+'.png'
            urllib.urlretrieve(imgurl,filename)

    '''
      获取网页地址
    '''
    def geturl(self,ctype,pages):
        urls=[]
        for i in range(1,pages+1):
            if i==1:
                url='http://movie.kankan.com/type/%s/' %(ctype)
                urls.append(url)
            else:
                url='http://movie.kankan.com/type/%s/page%d/'%(ctype,i)
                urls.append(url)

        movies={}
        for url in urls:
            print url
            headers ={
                "Host":"kkpgv2.kankan.com",
                "Connection":"keep-alive",
                "Referer": url,
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
            }
            request=urllib2.Request(url,None,headers)
            try:
                response=urllib2.urlopen(request,timeout=10)
                html=response.read().decode('utf8')
            except urllib2.URLError,e:
                if isinstance(e.reason,socket.timeout):
                    print "Exception:timeout"


            soup=BeautifulSoup(html)
            content=soup.find('ul',{'class':'movielist','id':'movie_list'})
            movieslists=content.findAll('a',{'href':re.compile(r'http://vod.kankan.com/v/[0-9]{2}/[0-9]{4,}\.shtml')})
            for movie in movieslists:
                movies[movie.get('title')]=movie.get('href')

        movieids=[]
        pattern=re.compile(r'http://vod.kankan.com/v/[0-9]{2}/([0-9]{4,})\.shtml')
        for title,url in movies:
            print title,url
            movieid=pattern.search(url).group(1)
            movieids.append(movieid)

        #结果保存
        f=open(type,'w')
        res='\n'.join(movieids)
        f.write(res)
        f.close()

    '''
       teleplay|tv|anime|movie
    '''
    def getmovied(self):
        objs={'teleplay':42,'tv':45,'anime':23,'movie':130}
        for ctype,num in objs.iteritems():
            print ctype,num
            self.geturl(ctype,num)



# 测试入口
if __name__ == "__main__":
    mex=mBS4Ex()
    mex.getmovied()

