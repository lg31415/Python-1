# -*- coding: utf-8 -*-
'''
    Fun:web自动化测试工具selenium
    Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
    State：
    Date:2017/4/28
    Author:tuling56
'''
import re,os, sys
import hues
import time

reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


'''
    selenium+webdriver浏览器
    tips:主要在于模拟手工操作
'''
class SelBrowser():
    def __init__(self,interface=False,browser='Chrome'):
        if browser=='Chrome':
            profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Google\\Chrome\\User Data'
            chrome_options=webdriver.ChromeOptions()
            if not interface:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
            self.driver=webdriver.Chrome(chrome_options=chrome_options) # 打开浏览器的时候带cookie
        elif browser=='Firefox':
            profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Mozilla\\Firefox\\Profiles\rh7qc3tr.default'
            profile_option=webdriver.FirefoxProfile(profile_dir)
            self.driver=webdriver.Firefox(profile_option)
        else:
            print "wrong browser parammeters"
            sys.exit()
        #self.driver.maximize_window()
        hues.info("浏览器初始化完毕")


    def __del__(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception,e:
            s=sys.exc_info()
            print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)

    # 演示
    def demo(self,url=''):
        self.driver.get('http://www.baidu.com')
        print self.driver.title
        #print self.driver.page_source.encode('utf8')
        #print self.driver.find_element_by_id('pagelet-myrepinlist').screenshot('zhah.png')  #截取快照
        #print self.driver.find_element_by_tag_name('body').screenshot('body.png')  #截取快照
        time.sleep(5)


    # cookie操作
    def cookie(self,url=''):
        # 获取cookie
        self.driver.get('http://toutiao.com/user/3163731884/pin/')
        cookielist=self.driver.get_cookies()
        print "cookie",cookielist
        for cookiedict in cookielist:
            print cookiedict['name'],'="',cookiedict['value'],'"'
            #for k,v in cookiedict.items():
            #   print k,v

        # 设置cookie
        with open('toutiao_cookie.log','r') as f:
            for line in f:
                try:
                    kvs=line.strip('\n').split(';')
                    for kv in kvs:
                        name,value=kv.split('=')
                        value=value.strip('"')
                        print name,'-->',value
                        self.driver.add_cookie({'name':name,'value':value})
                except Exception,e:
                    print str(e)

        self.driver.get('http://toutiao.com/user/3163731884/pin/')
        time.sleep(1)

    # 滚动条
    def mousemove(self,url=''):
        self.driver.get('http://www.baidu.com/')
        #assert "百度" in self.driver.title
        elem=self.driver.find_element_by_id("kw")
        elem.send_keys("张二狗"+Keys.RETURN)
        time.sleep(2)
        try:
            #js="var q=document.documentElement.scrollTop=10000"  #firfox浏览器
            js="var q=document.body.scrollTop=10000"        # chrome浏览器
            self.driver.execute_script(js)
            time.sleep(2)
        except NoSuchElementException:
            assert 0,u"找不到搜索的元素"

        self.driver.close()

    # 翻页
    def pagenext(self,url=''):
        self.driver.get('http://yinyue.kankan.com/list/hits/54.html')
        try:
            nextpage=self.driver.find_element_by_id('pagenav_next')
            while nextpage:
                nextpage.click()        #模拟点击
                cururl=self.driver.current_url
                print "当前页：",cururl
                self.driver.get(cururl)
                self.driver.implicitly_wait(1)
                nextpage=self.driver.find_element_by_id('pagenav_next')
            else:
                print '最后一页了'
        except Exception,e:
            print str(e)

    # 定位
    def location(self,url=''):
        file_path = 'file:///' + os.path.abspath('checkbox.html')
        self.driver.get(file_path)
        # 多元素选择
        '''
        self.driver.implicitly_wait(1)
        print self.driver.title
        inputs = self.driver.find_elements_by_tag_name('input')
        for input in inputs:
            if input.get_attribute('type') == 'checkbox':
                input.click()
                time.sleep(1)
        '''

        # css选择器选择
        '''
        #c1=self.driver.find_element_by_css_selector('.control-group-1 input[id="c1.1"]')
        c1=self.driver.find_element_by_css_selector('.control-group-1 label[class="control-label"]')
        c1.text='hahah'  # 不可修改的
        print c1.text
        '''

        # xpath选择器
        self.driver.get('http://www.jianshu.com/')
        c2s=self.driver.find_elements_by_xpath('//*[@id="list-container"]/ul/li')
        for c2 in c2s:
            c2t=c2.find_element_by_css_selector('a[class="title"]')
            print c2t.text


# 测试入口
if __name__ == "__main__":
    selbrowser=SelBrowser(interface=True,browser='Chrome')
    selbrowser.demo()
    #selchrome.pagenext()
    #selchrome.location()

