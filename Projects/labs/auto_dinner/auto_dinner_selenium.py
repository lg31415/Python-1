#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:模拟点击进行订餐
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
    模拟点击点餐
'''
class AutoDinnerSelium():
    def __init__(self):
        self.__init_db()
        self.__init_browser()

    # 浏览器初始化
    def __init_browser(self,interface=True):
        try:
            profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Google\\Chrome\\User Data'
            chrome_options=webdriver.ChromeOptions()
            if not interface:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
            self.driver=webdriver.Chrome(chrome_options=chrome_options) # 打开浏览器的时候带cookie
        except Exception,e:
            print "谷歌浏览器初始化失败"
            sys.exit()

    # 数据表初始化
    def __init_db(self):
        self.conn=sqlite3.connect('dinner.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists dinner_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime)')
        self.cursor.execute('create table if not exists history_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime)')
        self.cursor.execute('create table if not exists rank_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime)')

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.driver.quit()
        self.driver.close()

    def insert_db(self,rows):
        self.cursor.execute("insert into dinner_info(date,rest,menu,insert_time) values (strftime('%Y%m%d','now'),'美味通','好吃的',datetime())")
        self.conn.commit()

    def parse_dinner(self):
        self.driver

    def parse_history(self):
        pass

    def parse_rank(self):
        pass

    def parse(self):
        self.driver.get('http://dingcan.xunlei.cn/meal/')
        tags=self.driver.find_elements_by_xpath('//nav[@class="nav"]/ul/li')
        for tag in tags:
            print tag.text



# 测试入口
if __name__ == "__main__":
    asel=AutoDinnerSelium()
    asel.parse()
