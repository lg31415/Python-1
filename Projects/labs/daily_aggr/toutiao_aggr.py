#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
        Fun:自动登录头条的收藏，获取文章信息
        Ref:
        State：
        Date:2017/7/16
        Author:tuling56
'''
import re,os, sys
import hues
import time
import json
import requests
import MySQLdb
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

reload(sys)
sys.setdefaultencoding('utf-8')


class CToutiaoAggr():
    def __init__(self):
        self.collect_url='http://www.toutiao.com/c/user/3163731884/?tab=favourite'
        self.collect_url='http://www.toutiao.com/c/user/favourite/?page_type=2&user_id=3163731884&max_behot_time=0&count=20&as=A135C9B6EBE0F87&cp=596BC0EF38C7DE1&max_repin_time=0'
        self.cookiefile="toutiao_cookie.txt"
    def __build_cookie(self):
        cookies={}
        with open(self.cookiefile,'r') as f:
            for line in f:
                name_values=line.strip().split(';')
                for name_value in name_values:
                    name,value=map(str,name_value.split('='))
                    cookies[name]=value
        print cookies

    def get_collect(self):
        mcookie=self.__build_cookie()
        r=requests.get(self.collect_url,cookies=mcookie)
        print 'response_headers:',r.headers
        print 'response_cookies:',r.cookies
        if cmp(mcookie,r.cookies)==0:
            hues.info('cookie返回相同')
        print r.text


class CrawlerBase():
    def __init__(self):
        self.driver=webdriver.Chrome()
        self.__conn=MySQLdb.connect("localhost","root","123","media_lib",3316)
        self.__cursor = self.__conn.cursor()

    def __del__(self):
        try:
            self.driver.quit()
            self.driver.close()
            self.__conn.close()
            self.__cursor.close()
        except Exception,e:
            print "destroy exception:",str(e)

    def _entry_db(self,url,rurl,rimg,rtitle):
        sql = "replace into qq_relation_info set pageurl='%s',pageurlhash=md5(pageurl),relation_url='%s',relation_img='%s',relation_title=%s,insert_time=unix_timestamp(NOW())"%(url,rurl,rimg,self.__conn.escape(rtitle))
        sql = sql.decode("utf8").encode("gb18030")
        print sql
        self.__cursor.execute(sql)


    def get_html(self,url):
        # 静态请求
        #response = urllib2.urlopen(self.url)
        #text = response.read()  # .decode('utf8')

        # 动态请求
        self.driver.get(url)
        #js="var q=document.body.scrollTop=10000"             # phantomjs浏览器(通过)
        #js="var q=document.documentElement.scrollTop=10000"  # firfox浏览器
        js="var q=document.body.scrollTop=10000"              # chrome浏览器（通过,不带cookie啊）
        self.driver.execute_script(js)
        time.sleep(2)
        self.driver.implicitly_wait(10)
        content=self.driver.page_source.encode('utf8')        # #怀疑这部分是动态加载的,需要用phatomjs来做,依然是没法加载的
        self.html = etree.HTML(content)

        f=open('res.html','w')
        f.write(content)
        f.close()

        # 静态加载
        #self.html=etree.parse('iqiyi_recomm.html')
        #self.html=etree.HTML(open(cid+'.html').read().decode('utf8'))

    def get_json(self,url):
        jsondata=url
        try:
            self.json=json.loads(jsondata)
        except Exception,e:
            hues.warn(str(e))

    # 解析html（模拟浏览器加载）
    def parse_html(self,url):
        self.get_html(url)
        recomm_ul_list = self.html.xpath('//*[@id="leftdown_content"]/div[7]/div[2]/div/ul') # 为你推荐
        if not recomm_ul_list:
            hues.error("找不到推荐列表，请核对")
            return ''
        for ul_item in recomm_ul_list:
            li_list = ul_item.xpath('./li')
            for li_item in li_list:
                rtitle = li_item.xpath('./strong/a/text()')[0].encode('utf8')
                rurl = li_item.xpath('./strong/a/@href')[0].encode('utf8')
                rimg = li_item.xpath('./a/img/@src')[0].encode('utf8')
                self._entry_db(url,rurl,rimg,rtitle)

                hues.success("rtitle:" + rtitle)
                hues.success("rurl:" + rurl)
                hues.success("rimg:" + rimg)

    # 解析json（模拟js请求）
    def parse_json(self,url):
        self.get_json(url)
        try:
            recomlist=self.json['recItemList']
            for rec in recomlist:
                cid=rec['itemId']
                rurl="https://v.qq.com/x/cover/"+cid+".html".encode('utf8')
                rimg=rec['unionInfo']['vertical_pic_url'].encode('utf8')
                rtitle=rec['unionInfo']['title'].encode('utf8')
                self._entry_db(url,rurl,rimg,rtitle)

                hues.success("rtitle:" + rtitle)
                hues.success("rurl:" + rurl)
                hues.success("rimg:" + rimg)
        except Exception,e:
            hues.warn(str(e))



# 测试入口
if __name__ == "__main__":
    #ctag=CToutiaoAggr()
    #ctag.get_collect()
    url='http://www.toutiao.com/c/user/favourite/?page_type=2&user_id=3163731884&max_behot_time=0&count=20&as=A135C9B6EBE0F87&cp=596BC0EF38C7DE1&max_repin_time=0'
    cb=CrawlerBase()
    cb.get_html(url)
