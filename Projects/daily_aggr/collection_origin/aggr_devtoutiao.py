# -*- coding: utf-8 -*-
'''
    Fun:开发者头条收藏抓取
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

from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.common.keys import Keys


'''
   开发者头条收藏抓取
'''
class TuikuAggr():
    def __init__(self,interface=False,browser='Chrome'):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'media_lib')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
        self.pattern=re.compile(r'[^\d\s\-:]?')  # 替换模式
        self._init_browser(interface,browser)

    # 浏览器初始化
    def _init_browser(self,interface,browser):
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
        self.cursor.close()
        self.conn.close()
        self.driver.quit()
        self.driver.close()

    def _transcode(self, content):
        content = MySQLdb.escape_string(content)
        return content

    # 登录态解析条目
    def process_item_login(self,item):
        # 初始设置
        source='开发者头条'
        comment_num=0
        
        # 标题和链接
        try:
            target=item.find_element_by_xpath('.//h3[@class="title"]/a')
            title=target.text
            pageurl=target.get_attribute("href")
            m_md5 = hashlib.md5()
            m_md5.update(pageurl)
            pageurlhash = self._transcode(m_md5.hexdigest())
        except Exception,e:
            hues.error("解析标题和链接失败:\n"+str(e))
            return

        # 评论
        try:
            comment_num=item.find_element_by_xpath('.//i[@class="fa fa-comment"]')
            comment_num=comment_num.text
            if comment_num:
                comment_num=0
        except Exception,e:
            hues.error("评论提取失败:\n"+str(e))

        # 入库信息汇总
        hues.info("入库信息============")
        print "title:",title
        print "pageurl:",pageurl
        print "comment_num:",comment_num

        # 数据入库
        try:
            sql="replace into collection_base_info(pageurl,pageurlhash,title,source,comment_num,insert_time) values('%s','%s','%s','%s','%s',%s)"
            paras=(pageurl,pageurlhash,title,source,comment_num,'now()')
            sql=sql % paras
            hues.log(sql.decode('utf-8').encode('utf-8'))
            m=self.cursor.execute(sql.decode('utf-8').encode('utf-8'))
            print 'replace into collection_base_info:',title,"------>ret = ",m
        except Exception,e:
            hues.warn(str(e))

    # 登录状态
    def tuiku_aggr_login(self):
        self.driver.get('https://toutiao.io/favorites')
        next_page=self.driver.find_element_by_xpath('//ul[@class="pagination"]/li[last()-1]/a')
        last=False
        while next_page.text==u'下一页 ›' or last:
            cururl=self.driver.current_url
            hues.info("cur crawler:%s" %(cururl))
            items=self.driver.find_elements_by_xpath('//*[@class="posts posts-favorites"]/div')
            if len(items)==0:
                break
            for item in items:
                self.process_item_login(item)
            if last:
                break
            next_page.click()
            next_page=self.driver.find_element_by_xpath('//ul[@class="pagination"]/li[last()-1]/a')
            if next_page.text!=u"下一页 ›":
                last=True


# 测试入口
if __name__ == "__main__":
    selbrowser=TuikuAggr(interface=True,browser='Chrome')
    selbrowser.tuiku_aggr_login()
