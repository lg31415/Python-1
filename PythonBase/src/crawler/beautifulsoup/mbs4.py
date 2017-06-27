#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：beautifoul soup的使用
  参考网址：http://wiki.jikexueyuan.com/project/python-crawler-guide/beautiful-soup.html
'''



from bs4 import BeautifulSoup    #html
from bs4 import BeautifulStoneSoup  #xml
from bs4 import Tag,NavigableString
import urllib
import urllib2
import os,re
import socket


'''
    BS4基本使用
'''
class mBS4():
    def __init__(self):
        self.soup=BeautifulSoup(open('bs4-sample.html'))

    # 基础演示
    def bsdemo(self):
        #print self.soup.prettify() #,soup.html
        #获取所有内容
        #for string in self.soup.stripped_strings:
        #    print (repr(string))
        ps=self.soup.find('p')  #直接返回一个
        print '---',self.soup.p

        # 修改标题
        print "原标题:",self.soup.title.string
        self.soup.title.string='这是新标题'


    # 添加元素和设置元素属性
    def add_elem(self):
        p = self.soup.find('p')
        tag =self.soup.new_tag("span")
        tag['style']="position: absolute;  background-color:#888888;top: 0; z-index:9999999999999;right: 0;color:red"
        tag.string = 'pv:{pv} uv{uv}'.format(pv=12,uv=3)
        p.insert_after(tag)
        #print self.soup.prettify().decode('utf8')

        # 结果保存
        f=open('new.html','w')
        f.write(self.soup.prettify().decode('utf8'))
        f.close()

    # 高级查找（查找div#id2下的第一个p标签）
    def search_elem(self):
        obj=self.soup.find(id="id2")
        #print obj.text   # 输出该标签下所有的文本内容
        #for cc in obj.strings:
        #    print cc
        for par in obj.next_elements:
            if isinstance(par,Tag):
                if par.has_attr('id') and par['id']=='id3':
                    par['class']='cluce'
                print par.prettify()
            #else:
            #    print par.string

    # 查找by css
    def search_by_css(self):
        tarobj=self.soup.find(id="id2")
        tarobj.select('ul > li > a') # 这个要求子节点（而不是能后代节点）


    # 保存
    def saveres(self):
        res=self.soup.prettify().encode('utf8')
        f=open('bs4-result.html','w')
        f.write(res)
        f.close()



'''
    程序入口
'''
if __name__ == "__main__":
    mbs4=mBS4()
    mbs4.bsdemo()
    #mbs4.modfiy()
    #mbs4.search_elem()
    mbs4.saveres()
