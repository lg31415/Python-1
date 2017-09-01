# -*- coding: utf-8 -*-
'''
    Fun:浏览器初始化
    Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
    State：
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



'''
   爬虫浏览器基类
'''
class BrowserBase(object):
    def __init__(self,interface=False,browser='Chrome'):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'media_lib')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
        self._init_browser(interface,browser)

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.driver.quit()
        self.driver.close()

    def by_browser(self,browers='Chrome'):
        from selenium import webdriver
        if browser=='Chrome':
            self.__init_chrome_browser()
        elif browser=='Firefox':
            self.__init_firefox_browser()
        elif browser=='PhantomJS':
            self.__init_phantomjs_browser()
        else:
            hues.error("wrong browsers")
            return
        hues.info("浏览器初始化完毕")


    def __init_chrome_browser(self,interface=False):
        profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Google\\Chrome\\User Data'
        chrome_options=webdriver.ChromeOptions()
        if not interface:
            chrome_options.add_argument("--headless")
            if False:  # 无界面模式下要使用cookie，不然无界面的时候不会加载用户的配置文件，授权登录失败
                with open('csdn_chrome_cookie.ck','r') as f:
                try:
                    chrome_cookies=json.load(f,encoding='utf-8')#,object_pairs_hook=OrderedDict)
                    for ck in chrome_cookies:
                        self.driver.add_cookie({'domain':ck['domain'],'path':ck['path'],'name':ck['name'],'value':ck['value']})
                        return
                except Exception,e:
                    hues.error('解析chrome_cookies失败:',str(e))

        chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
        self.driver=webdriver.Chrome(chrome_options=chrome_options) # 打开浏览器的时候带cookie
        #self.driver.maximize_window()

    def __init_firefox_browser(self):
        profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Mozilla\\Firefox\\Profiles\rh7qc3tr.default'
        profile_option=webdriver.FirefoxProfile(profile_dir)
        self.driver=webdriver.Firefox(profile_option)
        #self.driver.maximize_window()

    def __init_phantomjs_browser(self):
        self.driver=webdriver.PhantomJS()
        #self.driver.maximize_window()


    def by_cookies(self,method="requests"):
        if method=='requests':
            self.__init_requests_cookies(self)  # 返回会话session对象
        elif method=='urllib2':
            self.__init_urllib2_cookies(self)    # 返回带cookie的opener对象
        else:
            hues.error("其它cookies的使用方法待添加,目前只有requests和urllib2")
            return

    def __init_requests_cookies(self):
        import requests
        # 将chrome浏览器的edit_plus_this_cookie插件导出的cookie为requests库使用
        with open('xxx_chrome_cookies.ck','r') as f:
            try:
                chrome_cookies=json.load(f,encoding='utf-8')#,object_pairs_hook=OrderedDict)
                for ck in chrome_cookies:
                    self.sess.cookies.set(ck['name'],ck['value'])
            except Exception,e:
                hues.error('解析chrome_cookies失败:',str(e))

    def __init_urllib2_cookies(self):
        # urllib2_cookie的方法有问题(需要将firefox导出的cookie进行转换)
        import urllib2
        import cookielib
        cookie = cookielib.MozillaCookieJar(self.cookies_file)
        handler = urllib2.HTTPCookieProcessor(cookie)
        self.opener = urllib2.build_opener(handler)
        urllib2.install_opener(self.opener)





# 测试入口
if __name__ == "__main__":
    pass
