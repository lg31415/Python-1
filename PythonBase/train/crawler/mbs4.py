#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：beautifoul soup的使用
  参考网址：http://wiki.jikexueyuan.com/project/python-crawler-guide/beautiful-soup.html
'''


from bs4 import BeautifulSoup    #html
from bs4 import BeautifulStoneSoup  #xml
import urllib
import urllib2
import os,re
import socket


htmlcontent =open('../../data/bs4html.html')

class mBS4():
    def __init__(self,html):
        self.url=None
        self.html=html
        self.soup=BeautifulSoup(self.html)
    def psdemo(self):
        #print self.soup.prettify() #,soup.html
        #获取所有内容
        #for string in self.soup.stripped_strings:
        #    print (repr(string))
        ps=self.soup.find('p')  #直接返回一个
        print ps
        print '---',self.soup.p


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


if __name__ == "__main__":

    mbs4=mBS4(htmlcontent)
    mbs4.psdemo()

    #mex=mBS4Ex()
    #mex.getmovied()