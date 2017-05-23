# -*- coding: utf-8 -*-
import scrapy
from myfirstscrapy.items import MyfirstscrapyItem
import logging

'''
    爬虫主体：负责处理请响应内容及url，处理完后交给pipline
'''
class MyfirstscrapySpider(scrapy.Spider):
    name = "myfscrapy"
    allowed_domains = ["njupt.edu.cn"]
    start_urls = [ "http://news.njupt.edu.cn/s/222/t/1100/p/1/c/6866/i/1/list.htm",]

    # 主解析函数
    def parse(self, response):
        news_page_num = 14
        page_num = 386
        if response.status == 200:
            for i in range(2,page_num+1):
                for j in range(1,news_page_num+1):
                    item = MyfirstscrapyItem()          # 导入item
                    item['news_url'],item['news_title'],item['news_date'] = response.xpath(
                    "//div[@id='newslist']/table[1]/tr["+str(j)+"]//a/font/text()"
                    "|//div[@id='newslist']/table[1]/tr["+str(j)+"]//td[@class='postTime']/text()"
                    "|//div[@id='newslist']/table[1]/tr["+str(j)+"]//a/@href").extract()
                  
                    yield item  #通过yield item来将存储下来的item交由后续的pipelines处理
                    
                next_page_url = "http://news.njupt.edu.cn/s/222/t/1100/p/1/c/6866/i/"+str(i)+"/list.htm"    # 之后通过生成next_page_url来通过scrapy.Request抓取下一页的新闻信息
                yield scrapy.Request(next_page_url,callback=self.parse_news)

    # 回调函数
    def parse_news(self, response):
        news_page_num = 14
        if response.status == 200:
            for j in range(1,news_page_num+1):
                item = MyfirstscrapyItem()
                item['news_url'],item['news_title'],item['news_date'] = response.xpath(
                "//div[@id='newslist']/table[1]/tr["+str(j)+"]//a/font/text()"
                "|//div[@id='newslist']/table[1]/tr["+str(j)+"]//td[@class='postTime']/text()"
                "|//div[@id='newslist']/table[1]/tr["+str(j)+"]//a/@href").extract()
                yield item