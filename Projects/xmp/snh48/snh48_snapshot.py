#!/usr/bin/env pythonana
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：片库动漫、电视剧，综艺，电影页数据展示
  改进说明：restful api格式
'''

import json
import urllib2
import os
import re
import sys
from datetime import date,  datetime, timedelta
from bs4 import BeautifulSoup,Tag

from selenium import  webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys



reload(sys)
sys.setdefaultencoding('utf8')

curdir=os.getcwd()
datapath=curdir.replace("/bin","/data")

'''
    关键还是在定位
'''
class MapHot():
    def __init__(self,url,hotdata,dsturl):
        driver=webdriver.PhantomJS()
        driver.get(url)
        page_content=driver.page_source.encode('utf8')
        #response=urllib2.urlopen(url)
        #page_content=response.read().decode('utf8')
        self.soup=BeautifulSoup(page_content,"lxml")
        self.hotdata=hotdata
        self.dst_html= dsturl
        self.posnum={}

    # _展示函数
    def _add_display(self,obj,pv,uv,flag=False):
        tag =self.soup.new_tag("span")
        tag['style']="position:absolute; background-color:yellow;top: 0; z-index:9999999999999;left:0;color:red;opacity:0.8;"
        tag.string = 'pv:{pv} uv:{uv}'.format(pv=pv,uv=uv)
        if  flag:
            obj.insert(1,tag)
        else:
            obj.insert_before(tag)

    # _位置解析(以位置串为例)  
    # _DIV[6]_DIV[0]_DIV[1]_UL[0]_LI[5]_P[0]_A[0]  
    # poster1_A[0]
    # poster1_UL[1]_LI[0]_A[0]
    def _getposmark_hpos(self,pos_r):
        bractpos=pos_r.find('[')
        if bractpos!=-1:
            bractstr=pos_r[:bractpos]
            posmark='_'.join(bractstr.split('_')[:-1])
            if posmark!='':
                lpos=pos_r.replace(posmark+'_','').split('_')
            else:
                posmark='body'
                lpos=pos_r[1:].split('_')
        else:
            posmark=pos_r
            lpos=[]

        #print "\033[1;31m[解析的位置是]\033[0m:",posmark,"--->",lpos
        return posmark,lpos


    # 位置解析
    def posnum_parse(self):
        with open(self.hotdata,'r') as f:
            for line in f:
                try:
                    pos,pv,uv=line.strip().split()
                    posmark,hpos=self._getposmark_hpos(pos)
                    lpr=re.compile(r'[\[\]]')
                    lpl=[]
                    for lp in hpos:
                        elnum=re.split(lpr,lp)[:-1]
                        lpl.append((elnum[0].lower(),int(elnum[1])))
                    lpl.append((pv,uv))                                 # 最底层是pv和uv数据
                    self.posnum.setdefault(posmark,[]).append(lpl)      # 最外层是定位标示，内部是定位的规律
                except Exception,e:
                    print u"解析位置失败",line
                    print str(e)
        #print self.posnum

    # 修改页面
    def modify_html(self):
        for posmark,ghpos in self.posnum.iteritems():
            if posmark=='body':
                obj=self.soup.find('body')
            else:
                obj=self.soup.find(id=posmark)

            if not obj:
                print "Cann't find posmark={posmark}".format(posmark=posmark)
                continue

            flag=False
            for lhpos in ghpos:  #该定位符下的所有定位元素（除去最后一个，是pv和uv元组）
                try:
                    # --------------------------寻找开始--------------
                    el_obj=obj      # 最外层
                    for lhp in lhpos[:-1]:
                        el,num=lhp       # 元素和级别
                        el_list= [i for i in el_obj.contents if isinstance(i,Tag) and i.name==el.lower()]  # 选取所有的tag标签
                        el_obj=el_list[num]
                    # ------------------------- 寻找结束--------------
                    if el_obj.find('img'):
                        flag=True
                    self._add_display(el_obj,lhpos[-1][0],lhpos[-1][1],flag)
                except Exception,e:
                    print "\033[1;31m[添加数据显示失败]:\033[0m:",posmark,lhpos
                    print str(e)
        #print str(obj).decode('utf8')   #显示该list最后的解析结果

        # 最后结果保存
        res=self.soup.prettify().encode('utf8')
        f=open(self.dst_html,'w')
        f.write(res)
        f.close()


###########################  Process Flow ##########################
if __name__ == "__main__":
    if len(sys.argv)<2:
        stadate=date.today()-timedelta(days=1)
        stadate = '%04d%02d%02d' %(stadate.year, stadate.month, stadate.day)
    else:
        stadate=sys.argv[1]

    # 创建结果目录
    respath='./' #os.path.join(datapath,"pianku_"+stadate)
    if not os.path.exists(respath):
        os.mkdir(respath)

    # 依次循环处理每个页面

    url="http://48.fans.xunlei.com/index.shtml"
    dsturl='snh48_frontpage.html' #"{datapath}/pianku_{stadate}/{pagetype}_tuijian.shtml".format(datapath=datapath,stadate=stadate,pagetype=pagetype)
    hotdata="snh48_frontpage_click_20170512"#"{datapath}/{pagetype}_tuijian_{stadate}".format(datapath=datapath,pagetype=pagetype,stadate=stadate)
    print url
    mhot=MapHot(url,hotdata,dsturl)
    # 解析位置
    mhot.posnum_parse()
    # 修改页面
    mhot.modify_html()
