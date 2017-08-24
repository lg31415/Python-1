#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:使用cookie进行订餐
	Ref:
	State：
	Date:2017/8/24
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import sqlite3
import urllib2
import cookielib
from selenium import webdriver
from lxml import etree
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup


# 日期参数处理
mdate = date.today().strftime("%Y%m%d")


'''
    使用cookie点餐
'''
class AutoDinnerCookie():
    def __init__(self):
        self.__init_db()
        self.__init_browser()

    def __init_browser(self):
        cookie = cookielib.MozillaCookieJar()
        cookie.load('dinner_cookies.log', ignore_discard=True, ignore_expires=True)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

    def __init_db(self):
        self.conn=sqlite3.connect('dinner.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists dinner_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime)')
        self.cursor.execute('create table if not exists history_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime)')
        self.cursor.execute('create table if not exists rank_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime)')

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.opener.close()

    def insert_db(self,rows):
        self.cursor.execute("insert into dinner_info(date,rest,menu,insert_time) values (strftime('%Y%m%d','now'),'美味通','好吃的',datetime())")
        self.conn.commit()

    # 获取内容
    def _get_content(self):
        req = urllib2.Request("http://dingcan.xunlei.cn/meal/")
        response = self.opener.open(req)
        content=response.read().decode('utf-8').encode('utf-8')
        print content
        with open('dinner.html','w') as f:
            f.write(content)
        return content

    # 点餐
    def parse_dinner(self):
        pass

    # 历史
    def parse_history(self):
        pass

    # 排行
    def parse_rank(self):
        pass

    #　解析入口
    def parse(self):
        #content=self._get_content()
        #self.html=etree.HTML(content)
        self.html=etree.HTML(open('dinner.html','r').read())
        rests=self.html.xpath('//*[@class="rest_wrap"]/section')
        for rest in rests:
            rest_name=rest.xpath('.//h1[@class="rest_name"]/span/text()')
            rest_id=rest.xpath('@id')
            menus=rest.xpath('.//ul[@class="menu clearfix"]/li[@class!="carpet"]')
            print rest_name,"============="
            for menu in menus:
                menu_name=menu.xpath('./a/div[@class="dish_name"]/strong/text()')
                menu_id=menu.xpath('./a/@id')
                print menu_name



# 测试入口
if __name__ == "__main__":
    ad=AutoDinnerCookie()
    ad.parse_menu()
