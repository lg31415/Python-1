#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:python装饰器学习
	Ref:http://mp.weixin.qq.com/s/Ru_TpOnelMXPzH-1o34oZw
	State：
	Date:2017/5/17
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


import scrapy
from scrapy.selector import HtmlXPathSelector,XPathSelector
from myfirstscrapy.items import QQrecommItem
import requests

'''
    腾讯推荐视频爬虫
'''
class QQrecommSpider(scrapy.Spider):
    name = "qq_recomm_list"
    allowed_domains = ["v.qq.com"]
    start_urls = ["https://v.qq.com/x/cover/5a3aweewodeclku.html"]  #上古情歌

    def __init__(self):
        hues.info('QQrecommSpider初始化')

    def parse(self,response):
        hues.info('进入解析阶,响应体如下:')
        if response.status != 200:
            hues.error('response wrong code,%s' %(response.code))
            return

        '''
        hues.info("利用requests库进行响应请求")
        res=requests.get(self.start_urls[0])
        html=res.content
        #hues.log(html)
        hxs = XPathSelector(html)
        '''

        recomm_ul_list=response.xpath('//*[@id="leftdown_content"]/div[7]/div[2]/div/ul')
        if recomm_ul_list:
            hues.success("找到推荐页面，逐步遍历")
        for ul_item in recomm_ul_list:
            li_list=ul_item.xpath('./li')
            for li_item in li_list:
                qqrecomm_item= QQrecommItem()
                title=li_item.xpath('./strong/a/text()')
                ref_url=li_item.xpath('./strong/a/@href')
                poster_url=li_item.xpath('./a/img/@src')
                qqrecomm_item['item_title']=title
                qqrecomm_item['item_url']=ref_url
                qqrecomm_item['item_poster']=poster_url
                yield  qqrecomm_item

                hues.success("title:"+title)
                hues.success("url:"+ref_url)
                hues.success("poster:"+poster_url)
