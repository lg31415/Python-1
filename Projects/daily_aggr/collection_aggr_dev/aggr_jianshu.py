# -*- coding: utf-8 -*-
'''
    Fun:简书收藏和喜欢抓取
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
import requests
from bs4 import BeautifulSoup


'''
    简书收藏和喜欢抓取
'''
class JianshuAggr():
    def __init__(self):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'media_lib')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
        self.pattern=re.compile(r'[^\d\s\-【:】]?')  # 替换模式
        self.sess=requests.Session()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.sess.close()

    def _transcode(self, content):
        content = MySQLdb.escape_string(content)
        return content

    # 收藏解析
    def parse_item_collect(self,item):
        pass

    # 喜欢解析
    def parse_item_like(self,item):
        pass

    # 登录
    def login(self):
        postdata={}
        post_url=''
        self.post(post_url,data=postdata)

    # 收藏抓取
    def jianshu_aggr_favor(self):
        collect_url='http://www.jianshu.com/bookmarks'
        print "cookies:",self.cookies
        res=self.sess.get(collect_url).text
        self.soup=BeautifulSoup(res)
        print self.soup.prettify().encode('utf8')


    # 喜欢抓取
    def jianshu_aggr_like(self):
        like_url='http://www.jianshu.com/users/5cb84169d6bb/liked_notes'
        html=requests.get(like_url,cookies=self.cookies)
        self.soup=BeautifulSoup(html)


# 测试入口
if __name__ == "__main__":
    jaggr=JianshuAggr()
    jaggr.jianshu_aggr_favor()

