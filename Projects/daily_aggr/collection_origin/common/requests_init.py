# -*- coding: utf-8 -*-
'''
    Fun:requests会话对象cookie初始化
    Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
    State：
    Date:2017/4/28
    Author:tuling56
'''

import os,sys
import hues
import json
import requests
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')


'''
   爬虫requests库初始化（cookie方案）
'''
class RequestsBase(object):
    def __init__(self):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'labs')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
        self.sess=requests.Session()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.sess.close()  #关闭会话

    def htmlfilter(self,tagstring):
        p = re.compile(r'<[^>]+>')
        filtertag = p.sub("", tagstring)
        return filtertag

    # 将chrome浏览器的cookie为requests库使用
    def init_requests_cookie(self,cookie_file=''):
        hues.info("cookie初始化session对象")
        with open(cookie_file,'r') as f:
            try:
                chrome_cookies=json.load(f,encoding='utf-8')#,object_pairs_hook=OrderedDict)
                for ck in chrome_cookies:
                    self.sess.cookies.set(ck['name'],ck['value'])
            except Exception,e:
                hues.error('添加chrome_cookies失败:',str(e))