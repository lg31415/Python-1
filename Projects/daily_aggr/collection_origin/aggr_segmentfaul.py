# -*- coding: utf-8 -*-
'''
    Fun:segmentfaul抓取
    Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
    State：未完成
    Date:2017/4/28
    Author:tuling56
'''
import re,os, sys
import hues
import time
import MySQLdb
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')

import json
import urllib2
import cookielib
import requests
from bs4 import BeautifulSoup
from datetime import date,datetime

'''
    segmentfaul收藏和喜欢抓取
'''
class SegmentFaultAggr():
    def __init__(self):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'media_lib')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
        self.pattern=re.compile(r'[^\d\s\-【:】]?')  # 替换模式
        self.cookies_file='segmentfaul_cookies_chrome.ck'
        self.__login()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.opener.close()  #关闭会话
        self.sess.close()

    def _transcode(self, content):
        content = MySQLdb.escape_string(content)
        return content

    def __login(self):
        # urllib2_cookie的方法有问题
        cookie = cookielib.MozillaCookieJar(self.cookies_file)
        handler = urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(handler)
        urllib2.install_opener(self.opener)

        # requests_cookie
        # 将chrome浏览器的cookie为requests库使用
        self.sess=requests.Session()
        with open(self.cookies_file,'r') as f:
            try:
                chrome_cookies=json.load(f,encoding='utf-8')#,object_pairs_hook=OrderedDict)
                for ck in chrome_cookies:
                    self.sess.cookies.set(ck['name'],ck['value'])
            except Exception,e:
                hues.error('解析chrome_cookies失败:',str(e))

    # 单条目解析
    def parse_item(self,tags,item):
        source='segmentfault'
        tags=tags
        pageurlhash=''

        # 解析标题和链接
        try:
            titlehref=item.select('h2[class="title"] > a')[0]
            pageurl=titlehref.attrs.get('href','')
            if pageurl.startswith('/p'):
                pageurl='https://segmentfault.com'+pageurl
                m_md5 = hashlib.md5()
                m_md5.update(pageurl)
                pageurlhash = self._transcode(m_md5.hexdigest())
            title=titlehref.string
        except Exception,e:
            print "解析标题和链接失败,",str(e)
            return


        # 解析publish_time
        try:
            publish_time=item.find(class_=re.compile("author")).find('li').text
            if publish_time:
                res=re.search(u'(\d+)月(\d+)日',publish_time)
                publish_time='-'.join([str(date.today().year),res.groups()[0],res.groups()[1]])+' 00:00:00'
        except Exception,e:
            print "解析publish_time失败:",str(e)
            publish_time=''

         # 入库信息汇总
        hues.info("入库信息============")
        print "title:",title
        print "pageurl:",pageurl
        print "publish_time:",publish_time

        # 数据入库
        try:
            sql="replace into collection_base_info(pageurl,pageurlhash,title,tags,source,publish_time,insert_time) values('%s','%s','%s','%s','%s','%s',%s)"
            paras=(pageurl,pageurlhash,title,tags,source,publish_time,'now()')
            sql=sql % paras
            hues.log(sql.decode('utf-8').encode('utf-8'))
            m=self.cursor.execute(sql.decode('utf-8').encode('utf-8'))
            print 'replace into collection_base_info:',title,"------>ret = ",m
        except Exception,e:
            hues.warn(str(e))


    # 单收藏页解析
    def parse_collect_page(self,tags,collect_page_url):
        #r=self.opener.open(collect_page_url)
        #soup=BeautifulSoup(r.read())
        r=self.sess.get(collect_page_url)
        soup=BeautifulSoup(r.text)
        #print soup.prettify().encode('utf8')
        items=soup.select('section') #[class="stream-list__item hover-show"]
        for item in items:
            self.parse_item(tags,item)

    # 收藏抓取
    def segmentfautl_aggr_collect(self):
        collect_url='https://segmentfault.com/user/bookmarks'
        headers={
            "Referer":"https://segmentfault.com/u/zibuyuxu_ftu/bookmarks",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
        }
        #req=urllib2.Request(collect_url,headers=headers)
        #r=self.opener.open(req)
        #r=urllib2.urlopen(collect_url)
        #soup=BeautifulSoup(r.read())
        r=self.sess.get(collect_url)
        soup=BeautifulSoup(r.text)
        #print soup.prettify().encode('utf8')
        collects=soup.select('section')
        for collect in collects:
            href=collect.attrs.get('data-id','')
            tags=collect.attrs.get('data-name','')
            if href:
                collect_page_url='https://segmentfault.com/bookmark/'+href
                self.parse_collect_page(tags,collect_page_url)


# 测试入口
if __name__ == "__main__":
    sfaggr=SegmentFaultAggr()
    sfaggr.segmentfautl_aggr_collect()
