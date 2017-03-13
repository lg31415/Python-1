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


'''
    BS4基本使用
'''
htmlcontent =open('../../data/bs4html.html')
class mBS4():
    def __init__(self,html):
        self.url=None
        self.html=html
        self.soup=BeautifulSoup(self.html)
    def bsdemo(self):
        #print self.soup.prettify() #,soup.html
        #获取所有内容
        #for string in self.soup.stripped_strings:
        #    print (repr(string))
        ps=self.soup.find('p')  #直接返回一个
        print ps
        print '---',self.soup.p

    def modfiy(self):
        p = self.soup.find('p')
        tag =self.soup.new_tag("span")
        tag['style']="position: absolute;  background-color:#888888;top: 0; z-index:9999999999999;right: 0;color:red"
        tag.string = 'pv:{pv} uv{uv}'.format(pv=12,uv=3)
        p.insert_after(tag)
        #print self.soup.prettify()
        f=open('new.html','w')
        f.write(self.soup.prettify())
        f.close()




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




'''
    测试案例
'''
class MapHot():
    def __init__(self):
        response=urllib2.urlopen('http://v.xunlei.com')
        self.posnum={}
        self.html=response.read().decode('utf8')
        self.soup=BeautifulSoup(self.html)

    # _展示函数
    def _add_display(self,obj,pv,uv):
        tag =self.soup.new_tag("span")
        tag['style']="position: absolute;  background-color:#888888;top: 0; z-index:9999999999999;right: 0;color:red"
        tag.string = 'pv:{pv} uv{uv}'.format(pv=pv,uv=uv)
        obj.insert_after(tag)

    # _获取lisitid
    def _getlistid(self,pos):
        list_regrex=re.compile('.*list_[0-9]?')
        listmatch=re.match(list_regrex,pos)
        if listmatch is not None:
            listid=listmatch.group(0)
            listid=listid.strip('_')
            return  listid
        else:
            return ""


    # step1:解析地址和数量(这个解析的还有问题)
    def posnum_parse(self):
        list_regrex=re.compile('.*list_[0-9]?')
        ul_regrex=re.compile('(?<=UL\[)[0-9]{1,2}(?=\])')
        div_regrex=re.compile('(?<=DIV\[)[0-9]{1,2}(?=\])')
        li_regrex=re.compile(('(?<=LI\[)[0-9]{1,2}(?=\])'))
        p_regrex=re.compile(('(?<=P\[)[0-9]{1,2}(?=\])'))
        with open('C:\\Users\\xl\\PhpstormProjects\\Maphot\\pianku_part','r') as f:
            for line in f:
                pos_detail={}
                pos,pv,uv=line.strip().split()
                pos_detail['PV']=pv
                pos_detail['UV']=uv
                listmatch=re.match(list_regrex,pos)
                if listmatch is not None:
                    listid=listmatch.group(0)
                    listid=listid.strip('_')

                    divmatch=re.search(div_regrex,pos)
                    if divmatch is not None:
                        divid=divmatch.group(0)
                        pos_detail['DIV']=divid

                    ulsearch=re.search(ul_regrex,pos)
                    if ulsearch is not None:
                        ulid=ulsearch.group(0),
                        pos_detail['UL']=ulid[0]

                    lisearch=re.search(li_regrex,pos)
                    if lisearch is not None:
                        liid=lisearch.group(0)
                        pos_detail["LI"]=liid
                self.posnum.setdefault(listid,[]).append(pos_detail)
        print u"解析位置完成"
        print self.posnum


    '''
        要解析成有序字典，这样才能代表其原来的位置
    '''
    def posnum_parse_impl(self):
        pass


    # step2:修改网页内容
    def modfiy_parse(self):
        # 解析每个列表区域
        for listid in self.posnum.keys():
            obj_list = self.soup.select('#'+listid)[0]
            poss=self.posnum[listid]
            for pos in poss:
                divid=int(pos.get('DIV',-1))
                ulid=int(pos.get('UL',-1))
                liid=int(pos.get('LI',-1))
                pid=int(pos.get('P',-1))
                uv=int(pos.get('UV',-1))
                pv=int(pos.get('PV',-1))

                if divid!=-1:
                    obj_list_div=obj_list.select('div')[divid]
                if ulid!=-1:
                    obj_list_ul=obj_list.select('ul')[ulid]
                if liid!=-1:
                    obj_list_li=obj_list.select('li')[liid]

                obj=obj_list_li.select('a > img')[0]
                self._add_display(obj,pv,uv)            # 直接调用展示函数

        # 最后结果保存
        res=self.soup.prettify().encode('utf8')
        f=open('new.html','w')
        f.write(res)
        f.close()


    # 直接解析原始位置focus_list_0_UL[0]_LI[0]_A[0]，继承该id的元素都进行计算
    def direct_parse(self):
        with open('C:\\Users\\xl\\PhpstormProjects\\Maphot\\pianku_part','r') as f:
            for line in f:
                pos,pv,uv=line.strip().split()
                listid=self._getlistid(pos)
                obj_list=self.soup.find(id=listid)
                print str(obj_list).decode('utf8')   #怎么将这个数字体现出来

                # 要返回
                ppds=['ul','li','a']

                for ppd in ppds:
                    ppd1=obj_list.find_all(ppd)



'''
    程序入口
'''
if __name__ == "__main__":
    #mbs4=mBS4(htmlcontent)
    #mbs4.bsdemo()
    #mbs4.modfiy()

    #mex=mBS4Ex()
    #mex.getmovied()

    #测试案例
    mhot=MapHot()
    #mhot.possplit()
    mhot.modfiy_list()