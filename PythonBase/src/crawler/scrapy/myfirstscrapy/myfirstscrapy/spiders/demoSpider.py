#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:练手项目：南邮新闻标爬取
	Ref:
	State：
	Date:2017/5/24
	Author:tuling56
'''

import scrapy
from myfirstscrapy.items import NanuNewsItem

'''
    爬虫主体：负责处理请响应内容及url，处理完后交给pipline
'''
class DemoSpider(scrapy.Spider):
    name = "demo_list"
    allowed_domains = ["v.xunlei.com"]
    start_urls = [ "http://new.tudou.com/category/c_96_p_4.html",]

    # 主解析函数
    def parse(self, response):
        print response._url
        print response.request
        print response.headers
        #for k,v in vars(response).iteritems():
        #    print k
        return           

        news_page_num = 14
        page_num = 386
        if response.status == 200:
            for i in range(2,page_num+1):
                for j in range(1,news_page_num+1):
                    item = NanuNewsItem()          # 导入item
                    item['news_url'],item['news_title'],item['news_date'] = response.xpath(
                    "//div[@id='newslist']/table[1]/tr["+str(j)+"]//a/font/text()"
                    "|//div[@id='newslist']/table[1]/tr["+str(j)+"]//td[@class='postTime']/text()"
                    "|//div[@id='newslist']/table[1]/tr["+str(j)+"]//a/@href").extract()
                  
                    yield item  #通过yield item来将存储下来的item交由后续的pipelines处理

                # 之后通过生成next_page_url来通过scrapy.Request抓取下一页的新闻信息
                next_page_url = "http://news.njupt.edu.cn/s/222/t/1100/p/1/c/6866/i/"+str(i)+"/list.htm"
                yield scrapy.Request(next_page_url,callback=self.parse_news)
        else:
            print "响应失败"
