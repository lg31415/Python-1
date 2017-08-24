#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun: xpath语法测试
    Ref:http://www.runoob.com/xpath/xpath-examples.html
        https://segmentfault.com/q/1010000004879947（子节点处理）
        http://cuiqingcai.com/2621.html（节点内容修改）
        http://lxml.de/tutorial.html(lxml官方参考)
    State：完成基本使用，后期需要再完善
    Date:2017/5/15
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
from lxml import etree


'''
    xpath语法处理器（学习类）
'''
class CXPath():
    def __init__(self,isfile=True):
        self.url='http://list.v.xunlei.com/v,type/5,movie/page2/'
        self.file='xpath-sample.html'
        self.res='xpath-result.html'
        if isfile:
            self._xfile()
        else:
            self._xrespone()

    def _xrespone(self):
        response=urllib2.urlopen(self.url)
        text=response.read()#.decode('utf8')
        self.html=etree.HTML(text)

    def _xfile(self):
        self.html=etree.HTML(open(self.file,'r').read()) # 其等效于直接解析文件
        # html=etree.parse(self.file)

    # 获取文本
    def xtext(self):
        reslist=self.html.xpath('//*[@id="wrapper"]/div[3]/p//text()')
        print reslist
        restext=''.join(reslist).strip()
        print restext.replace(' ','')

        # xpath的string函数的使用
        property_list_reg = '//ul[@id="parameter2"]//li'
        property_lst = self.html.xpath(property_list_reg)
        for e in property_lst:
            print(e.xpath('string(.)'))
        #print(len(property_lst))

    # 获取属性
    def xpros(self):
        ress=self.html.xpath('//*[@id!="datatable"]')
        for res in ress:
            print res.attrib

    # 修改xml树
    def xmod(self):
        lr=self.html.xpath('//*[@id="wrapper"]/div[2]/ul/li[1]/a')[0]
        # 获取和修改属性
        print lr.get('href'),lr.attrib['href']
        lr.set('class','myclass')

        # 添加子节点
        newc=etree.SubElement(lr,'p',attrib={'class':'ccc'})
        newc.text=u"这是新添加节点的内容"

        # 创建节点并选择添加位置
        newe = etree.Element("p")
        newe.text = u"添加的新内容2"
        newe.attrib['class']='vvdddd'
        newe.attrib['id']='idddd'
        lr.append(newe)
        #lr.insert(0,newe)
        #print etree.tostring(lr.getparent(),pretty_print=True,encoding='utf8')

        print etree.tostring(lr,pretty_print=True,encoding='utf8')

        # 输出最后的整个节点
        #print etree.tostring(self.html,encoding='utf8',pretty_print=True)

    # 保存xml树
    def xsave(self):
        # 转换成文本后保存
        with open(self.res,'wb') as f:
            result=etree.tostring(self.html,encoding='utf8',pretty_print=True)
            f.write(result)
            f.close()

        #直接保存
        fileHandler = open(self.res, "wb")
        self.html.write(fileHandler, encoding="utf-8", xml_declaration=True, pretty_print=True)
        fileHandler.close()




# 测试入口
if __name__ == "__main__":
    mxpath=CXPath()
    mxpath.xpros()



