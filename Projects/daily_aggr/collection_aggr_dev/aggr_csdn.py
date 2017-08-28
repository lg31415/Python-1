# -*- coding: utf-8 -*-
'''
    Fun:CSDN收藏抓取
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
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.common.keys import Keys


'''
    CSDN收藏抓取
'''
class CSDNAggr():
    def __init__(self,interface=False,browser='Chrome'):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'media_lib')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
        self.pattern=re.compile(r'[^\d\s\-【:】]?')  # 替换模式
        #self._init_browser(interface,browser)
        self._init_cookies(interface,browser)

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

    # 初始化cookie的方式来获得权限
    def _init_cookies(self,interface,browser='PhantomJS'):
        if browser=='Chrome':
            print "使用%s浏览器" %(browser)
            chrome_options=webdriver.ChromeOptions()
            if not interface:
                chrome_options.add_argument("--headless")
            self.driver=webdriver.Chrome(chrome_options=chrome_options)
        elif browser=='PhantomJS':
            print "使用%s浏览器" %(browser)
            self.driver=webdriver.PhantomJS()
            self.driver.get('http://my.csdn.net/?ref=toolbar')
        else:
            print "wrong browser parammeters"
            sys.exit()

        with open('csdn_cookie.ck','r') as f:
            try:
                chrome_cookies=json.load(f,encoding='utf-8')#,object_pairs_hook=OrderedDict)
                for ck in chrome_cookies:
                    self.driver.add_cookie({'domain':ck['domain'],'path':ck['path'],'name':ck['name'],'value':ck['value']})
            except Exception,e:
                hues.error('解析chrome_cookies失败:',str(e))

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
        source='CSDN'
        publish_time=''
        abstract=''

        # 标题和链接
        try:
            target=item.find_element_by_xpath('span[@class="info"]/a')
            title=target.text
            pageurl=target.get_attribute("href")
            m_md5 = hashlib.md5()
            m_md5.update(pageurl)
            pageurlhash = self._transcode(m_md5.hexdigest())
        except Exception,e:
            hues.error("解析标题和链接失败:\n"+str(e))
            return

        # 日期
        try:
            publish_time=item.find_element_by_xpath('span[@class="time"]')
            publish_time=publish_time.text
            if not publish_time.startswith('20'):
                publish_time="2017-"+publish_time
        except Exception,e:
            hues.error("日期失败:\n"+str(e))

        # 评论注释
        try:
            abstract=item.find_element_by_xpath('div[@class="cont"]')
            abstract=abstract.text
        except Exception,e:
            hues.error("提取评论失败:\n"+str(e))

        # 入库信息汇总
        hues.info("入库信息============")
        print "title:",title
        print "pageurl:",pageurl
        print "publish_time:",publish_time
        # 数据入库
        try:
            sql="replace into collection_base_info(pageurl,pageurlhash,title,source,abstract,publish_time,insert_time) values('%s','%s','%s','%s','%s','%s',%s)"
            paras=(pageurl,pageurlhash,title,source,abstract,publish_time,'now()')
            sql=sql % paras
            hues.log(sql.decode('utf-8').encode('utf-8'))
            m=self.cursor.execute(sql.decode('utf-8').encode('utf-8'))
            print 'replace into collection_base_info:',title,"------>ret = ",m
        except Exception,e:
            hues.warn(str(e))

    def process_item_json(self,item):
        # 初始设置
        source='CSDN'
        publish_time=''
        abstract=''

        # 解析数据
        dt_title=item['dt_title']
        title=re.search(">(.*?)</a>",dt_title)
        if title:
            title=title.group(1)

        pageurl=re.search("href=\"(.*?)\"",dt_title)
        if pageurl:
            pageurl=pageurl.group(1).rstrip('#comments')
            m_md5 = hashlib.md5()
            m_md5.update(pageurl)
            pageurlhash = self._transcode(m_md5.hexdigest())


        abstract=item.get('dl_content','')
        abstract=re.sub('&lt;','',abstract)
        abstract=re.sub('&gt;','',abstract)
        abstract=re.sub('/p','',abstract)

        publish_time=item.get('dt_time','')
        if not publish_time.startswith('20'):
            if publish_time:
                publish_time='2017-'+publish_time
            else:
                if 'count_down' in abstract:
                    publish_time=re.search('<span class="count_down">(.*?)</span>',abstract)
                    if publish_time:
                        publish_time=publish_time.group(1)
                        if not publish_time.startswith('20'):
                            publish_time='2017-'+publish_time
                        abstract=''

        # 入库信息汇总
        hues.info("入库信息============")
        print "title:",title
        print "pageurl:",pageurl
        print "abstract:",abstract
        print "publish_time:",publish_time

        # 数据入库
        try:
            sql="replace into collection_base_info(pageurl,pageurlhash,title,source,abstract,publish_time,insert_time) values('%s','%s','%s','%s','%s','%s',%s)"
            paras=(pageurl,pageurlhash,title,source,abstract,publish_time,'now()')
            sql=sql % paras
            hues.log(sql.decode('utf-8').encode('utf-8'))
            m=self.cursor.execute(sql.decode('utf-8').encode('utf-8'))
            print 'replace into collection_base_info:',title,"------>ret = ",m
        except Exception,e:
            hues.warn(str(e))

    def csdn_aggr(self):
        self.driver.get('http://my.csdn.net/?ref=toolbar')
        next_page=self.driver.find_element_by_xpath('//*[@class="myNews"]//div[@class="more"]/a')
        curnum,prenum=0,0
        while True:
            items=self.driver.find_elements_by_xpath('//*[@class="myNews"]//div[@class="mine"]/ul/li')
            curnum=len(items)
            if curnum==0 or curnum<=prenum :
                break
            for item in items:
                self.process_item(item)

            next_page.click()
            next_page=self.driver.find_element_by_xpath('//*[@class="myNews"]//div[@class="more"]/a')
            prenum=curnum

    def csdn_aggr_json(self):
        pageno=1
        flag=True
        while flag:
            req_url="http://my.csdn.net/service/main/get_feed_all?pageno=%s&pagesize=10&username=tuling56" %(pageno)
            hues.info(req_url)
            self.driver.get(req_url)
            res=self.driver.find_element_by_tag_name('body').text.encode('utf8')
            res_json=json.loads(res)
            if not res_json['result']['my']:
                hues.warn("解析结束")
                break
            for item in res_json['result']['my']:
                self.process_item_json(item)
            pageno=pageno+1
            time.sleep(1)


# 测试入口
if __name__ == "__main__":
    selbrowser=CSDNAggr(interface=False,browser='Chrome')
    selbrowser.csdn_aggr_json()

