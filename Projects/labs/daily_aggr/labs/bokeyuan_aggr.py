# -*- coding: utf-8 -*-
'''
    Fun:博客园收藏抓取
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
   博客园收藏抓取
'''
class BokeAggr():
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


    def process_item(self,item):
        # 初始设置
        type=''
        source='博客园'
        tags=''
        poster=''
        read_num=0
        comment_num=0
        publish_time=''

        # 标题和链接
        try:
            target=item.find_element_by_xpath('.//div[@class="list_block"]/h2/a')
            title=target.text
            pageurl=target.get_attribute("href")
            m_md5 = hashlib.md5()
            m_md5.update(pageurl)
            pageurlhash = self._transcode(m_md5.hexdigest())
        except Exception,e:
            hues.error("解析标题和链接失败:\n"+str(e))
            return

        # 备注
        abstract=''
        try:
            abstract=item.find_element_by_xpath('.//div[@class="link_content"]/div')
            abstract=abstract.text
        except Exception,e:
            hues.error("解析备注失败:\n"+str(e))

        # types
        tags=''
        try:
            ftags=item.find_elements_by_xpath('.//div[@class="link_memo"]/span[@class="tag"]/a')
            for ftag in ftags:
                tags=tags+"/"+ftag.text
        except Exception,e:
            hues.error("解析类型失败:\n"+str(e))
        tags=tags.strip('/')

        # 入库信息汇总
        hues.info("入库信息============")
        print "title:",title
        print "pageurl:",pageurl
        print "tags:",tags
        print "abstract:",abstract
        print "read_num:",read_num
        print "comment_num:",comment_num
        print 'publish_time:',publish_time

        # 数据入库
        try:
            sql="replace into collection_base_info(pageurl,pageurlhash,poster,title,type,source,abstract,tags,read_num,comment_num,publish_time,insert_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s)"
            paras=(pageurl,pageurlhash,poster,title,type,source,abstract,tags,str(read_num),str(comment_num),publish_time,'now()')
            sql=sql % paras
            hues.info(sql.encode('utf-8'))
            m=self.cursor.execute(self._transcode(sql.encode('utf-8')))
            print 'replace into collection_base_info:',title,"------>ret = ",m
        except Exception,e:
            hues.warn(sql)

    # 方法１：模拟点击下一页
    def boke_aggr(self):
        self.driver.get('http://wz.cnblogs.com/')
        next_page=self.driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/a[last()]')
        next_url='http://wz.cnblogs.com/'
        while next_page.text=='Next >':
            cururl=self.driver.current_url
            hues.info("cur crawler:%s\next crawler:%s" %(cururl,next_url))
            items=self.driver.find_elements_by_xpath('//*[@id="wz_list"]/div')
            for item in items:
                self.process_item(item)

            next_page.click()
            next_page=self.driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/a[last()]')
            next_url=next_page.get_attribute('href')


# 测试入口
if __name__ == "__main__":
    selbrowser=BokeAggr(interface=True,browser='Chrome')
    selbrowser.boke_aggr()

