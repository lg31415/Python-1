# -*- coding: utf-8 -*-
import scrapy
from collection_aggr.items import CollectionAggrItem
#from scrapy.selector import HtmlXPathSelector

import re,os,sys
import hues
import time
import json
import requests
import MySQLdb
from lxml import etree
from selenium import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['toutiao.com']
    start_urls = ['http://www.toutiao.com/c/user/3163731884/?tab=favourite']

    def __init__(self,browser='Chrome'):
        if browser=='Chrome':
            profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Google\\Chrome\\User Data'
            chrome_options=webdriver.ChromeOptions()
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
        self.driver.quit()
        self.driver.close()

    def parse(self,response):
        self.driver.get('http://www.toutiao.com/c/user/3163731884/?tab=favourite')

        # 切换到收藏tab
        collecton_tab=self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[1]/ul/li[2]')
        collecton_tab.click()
        self.driver.implicitly_wait(3)

        # 模拟滚动
        now_total_num=0
        pre_total_num=0
        scroll_num=1
        start=0
        while True:
            if scroll_num!=1:
                hues.info("滚动下滑，继续抓取......")
                scroll_dis=10000*scroll_num
                js="var q=document.body.scrollTop=%s" %(scroll_dis)        # chrome浏览器
                self.driver.execute_script(js)
                time.sleep(4)
            items=self.driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div/ul/li')
            now_total_num=len(items)
            start_pos=start
            hues.info("now_total_num:"+str(now_total_num))
            hues.info("start_pos:"+str(start_pos))
            if now_total_num==pre_total_num:
                hues.warn("没有更新新内容,尝试再次刷新.....")
                self.driver.execute_script(js)
                time.sleep(4)
                items=self.driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div/ul/li')
                now_total_num=len(items)
                if now_total_num==pre_total_num:
                    hues.error("再次刷新后依然没有抓取到新内容，退出")
                    break
            for item in items[start_pos:]:
                items=CollectionAggrItem()
                items['pageurl']=''
                items['title']=''
                items['type']=''
                items['source']='toutiao'
                items['abstract']=''
                items['tags']=''
                items['publish_time']=''

                target=item.find_element_by_xpath('div/div[1]/div/div[1]/a')
                items['pageurl']=target.get_attribute("href")
                items['title']=target.text

                # author&pulish
                attach_info=item.find_element_by_xpath('div/div[1]/div/div[2]')
                read_num=attach_info.find_element_by_xpath('div[1]/a[1]').text
                m=re.search('d/+',read_num)
                if m:
                    read_num=m.group(0)
                author=attach_info.find_element_by_xpath('div[1]/a[2]').text
                publish_time=attach_info.find_element_by_xpath('div[1]/span').text
                items['publish_time']=publish_time

                start=start+1

                print "最终入库的内容如下："
                print "title:\t",items['title']
                print "pageurl:\t",items['pageurl']
                print "publish_time:\t",items['publish_time']

                yield items

            pre_total_num=now_total_num
            scroll_num=scroll_num+1

