# -*- coding: utf-8 -*-
'''
    Fun:谷歌浏览器初始化
    Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
    State：
    Date:2017/4/28
    Author:tuling56
'''

import os,sys
import hues
import json
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver

'''
   爬虫chrome浏览器基类（selenium方案）
'''
class ChromeBrowserBase(object):
    def __init__(self):
        hues.info("基类初始化")
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'labs')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
        self.chrome_interface=True

    def __del__(self):
        hues.info("基类析构")
        self.cursor.close()
        self.conn.close()
        self.driver.quit()
        self.driver.close()

    # 打开浏览器的时候自动带cookie
    def init_chrome_browser(self,profile_dir=''):
        hues.info("基类浏览器初始化")
        if not profile_dir:
            profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Google\\Chrome\\User Data'
        chrome_options=webdriver.ChromeOptions()
        if not self.chrome_interface:
            chrome_options.add_argument("--headless")  # 无界面模式还有些问题

        chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
        self.driver=webdriver.Chrome(chrome_options=chrome_options)
        #self.driver.maximize_window()

    # 手动为浏览器加载cookies(通过edit_this_cookies插件导出的)
    def init_chrome_cookie(self,chrome_cookie_file=''):
        hues.info("基类浏览器cookie初始化")
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # 无界面模式还有些问题
        self.driver=webdriver.Chrome(chrome_options=chrome_options)
        with open(chrome_cookie_file,'r') as f:
            try:
                chrome_cookies=json.load(f,encoding='utf-8')#,object_pairs_hook=OrderedDict)
                for ck in chrome_cookies:
                    self.driver.add_cookie({'domain':ck['domain'],'path':ck['path'],'name':ck['name'],'value':ck['value']})
            except Exception,e:
                hues.error('添加chrome_cookies失败:',str(e))

    # 接口
    def by_method(self,method,profile_dir='',chrome_cookie=''):
        if method=='browser':
            self.__init_chrome_browser(profile_dir)
        elif method=='cookie':
            self.__init_chrome_cookie(chrome_cookie)
        else:
            print "wrong method"