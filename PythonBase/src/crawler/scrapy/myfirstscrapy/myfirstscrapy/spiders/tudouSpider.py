#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
        Fun:tudou系列爬虫
        Ref:
        State：
        Date:2017/5/31
        Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


import scrapy
from myfirstscrapy.items import TudouItem


'''
    功能：土豆电视剧爬虫
'''
class TudouTeleplaySpiderBase(scrapy.Spider):
    name = "tudou_teleplay_list"
    allowed_domains = ["new.tudou.com"]
    start_urls = ["http://new.tudou.com/category/c_97.html"]

	# 控制解析的页数
    def __init__(self):
        self.page=1

    # 主解析函数
    def parse(self, response):
        self.page=self.page+1
        news_page_num = 30
        if response.status == 200:
            for j in range(1, news_page_num + 1):
                item = TudouItem()
                item['item_title'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@title').extract()[0]
                item['item_url'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@href').extract()[0]
                item['item_jishu'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[1]/div[2]/span').xpath('string(.)').extract()[0]
                print '\033[1;31m=====>item:\033[0m', item
                yield item
            if self.page>=40:     # 注意这个判断不能否在yield scrapy.Request之后，不然循环永远不会终止
                print "循环解析结束,解析40页"
                return
            next_page_url = "http://new.tudou.com/category/c_97_p_" + str(self.page) + ".html"
            print "\033[1;31m[===next_page_url===]\033[0m:",next_page_url
            yield scrapy.Request(next_page_url,callback=self.parse)
        else:
            print "响应失败"

'''
    功能：土豆电影爬虫
'''
class TudouMovieSpiderBase(scrapy.Spider):
    name = "tudou_movie_list"
    allowed_domains = ["new.tudou.com"]
    start_urls = ["http://new.tudou.com/category/c_96.html"]

	# 控制解析的页数
    def __init__(self):
        self.page=1

    # 主解析函数
    def parse(self, response):
        self.page=self.page+1
        news_page_num = 30
        if response.status == 200:
            for j in range(1, news_page_num + 1):
                item = TudouItem()
                item['item_title'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@title').extract()[0]
                item['item_url'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@href').extract()[0]
                item['item_jishu'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[1]/div[2]/span').xpath('string(.)').extract()[0]
                print '\033[1;31m=====>item:\033[0m', item
                yield item
            if self.page>=40:     # 注意这个判断不能否在yield scrapy.Request之后，不然循环永远不会终止
                print "循环解析结束,解析40页"
                return
            next_page_url = "http://new.tudou.com/category/c_96_p_" + str(self.page) + ".html"
            print "\033[1;31m[===next_page_url===]\033[0m:",next_page_url
            yield scrapy.Request(next_page_url,callback=self.parse)
        else:
            print "响应失败"


'''
    功能：土豆综艺爬虫
'''
class TudouTvSpiderBase(scrapy.Spider):
    name = "tudou_tv_list"
    allowed_domains = ["new.tudou.com"]
    start_urls = ["http://new.tudou.com/category/c_85.html"]

	# 控制解析的页数
    def __init__(self):
        self.page=1

    # 主解析函数
    def parse(self, response):
        self.page=self.page+1
        news_page_num = 30
        if response.status == 200:
            for j in range(1, news_page_num + 1):
                item = TudouItem()
                item['item_title'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@title').extract()[0]
                item['item_url'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@href').extract()[0]
                item['item_jishu'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[1]/div[2]/span').xpath('string(.)').extract()[0]
                print '\033[1;31m=====>item:\033[0m', item
                yield item
            if self.page>=40:     # 注意这个判断不能否在yield scrapy.Request之后，不然循环永远不会终止
                print "循环解析结束,解析40页"
                return
            next_page_url = "http://new.tudou.com/category/c_85_p_" + str(self.page) + ".html"
            print "\033[1;31m[===next_page_url===]\033[0m:",next_page_url
            yield scrapy.Request(next_page_url,callback=self.parse)
        else:
            print "响应失败"


'''
    功能：土豆动漫爬虫
'''
class TudouAnimalSpiderBase(scrapy.Spider):
    name = "tudou_animal_list"
    allowed_domains = ["new.tudou.com"]
    start_urls = ["http://new.tudou.com/category/c_100.html"]

	# 控制解析的页数
    def __init__(self):
        self.page=1

    # 主解析函数
    def parse(self, response):
        self.page=self.page+1
        news_page_num = 30
        if response.status == 200:
            for j in range(1, news_page_num + 1):
                item = TudouItem()
                item['item_title'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@title').extract()[0]
                item['item_url'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@href').extract()[0]
                item['item_jishu'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[1]/div[2]/span').xpath('string(.)').extract()[0]
                print '\033[1;31m=====>item:\033[0m', item
                yield item
            if self.page>=40:     # 注意这个判断不能否在yield scrapy.Request之后，不然循环永远不会终止
                print "循环解析结束,解析40页"
                return
            next_page_url = "http://new.tudou.com/category/c_100_p_" + str(self.page) + ".html"
            print "\033[1;31m[===next_page_url===]\033[0m:",next_page_url
            yield scrapy.Request(next_page_url,callback=self.parse)
        else:
            print "响应失败"


'''
    功能：土豆系列爬虫1
    问题：存在问题
'''
class TudouSpiderImpl1(scrapy.Spider):
    name = "tudou_all1_list"
    allowed_domains = ["new.tudou.com"]
    start_urls = ["http://new.tudou.com/category/c_97.html"]

    def __init__(self):
        self.page=1
        self.urls={'teleplay':["http://new.tudou.com/category/c_97.html",-1],
                    'movie':["http://new.tudou.com/category/c_97.html",-1],
                    'tv':["http://new.tudou.com/category/c_85.html",-1],
                    'animal':["http://new.tudou.com/category/c_100.html",-1]}

    def parse(self, response):
        news_page_num=30
        for ctype,urlflag in self.urls.iteritems():
            self.page=self.page+1
            url,flag=urlflag[0],urlflag[1]
            if urlflag==-1:
                continue
            if response.status == 200:
                for j in range(1, news_page_num + 1):
                   item = TudouItem()
                   item['item_title'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@title').extract()[0]
                   item['item_url'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@href').extract()[0]
                   item['item_jishu'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[1]/div[2]/span').xpath('string(.)').extract()[0]
                   print '\033[1;31m=====>item:\033[0m', item
                   yield item
                if self.page>=40:
                   print "循环解析结束,解析40页"
                   self.page=1
                   return

                next_page_url = url.replace(".html","") +"_p_"+str(self.page) + ".html"
                print "\033[1;31m[===next_page_url===]\033[0m:",next_page_url
                yield scrapy.Request(next_page_url,callback=self.parse)
            else:
                print '响应失败'


'''
    功能：土豆系列爬虫2
    利用爬虫的url指向
'''
class TudouSpiderImpl2(scrapy.Spider):
    name = "tudou_all2_list"
    allowed_domains = ["new.tudou.com"]
    start_urls = ["http://new.tudou.com/category/c_97.html"]

    def __init__(self):
        self.page=1
        self.urls={'teleplay':["http://new.tudou.com/category/c_97.html",-1],
                    'movie':["http://new.tudou.com/category/c_97.html",-1],
                    'tv':["http://new.tudou.com/category/c_85.html",-1],
                    'animal':["http://new.tudou.com/category/c_100.html",-1]}

    def parse(self, response):
        news_page_num=30
        for ctype,urlflag in self.urls.iteritems():
            print "self.page",self.page
            self.page=self.page+1
            url,flag=urlflag[0],urlflag[1]
            if flag==-1:
                self.urls[ctype][1]=0
            else:
                continue
            if response.status == 200:
                for j in range(1, news_page_num + 1):
                   item = TudouItem()
                   item['item_title'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@title').extract()[0]
                   item['item_url'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[2]/div[1]/a/@href').extract()[0]
                   item['item_jishu'] = response.xpath('//*[@id="category"]/div[3]/div['+str(j)+']/div/div[1]/div[2]/span').xpath('string(.)').extract()[0]
                   #print '\033[1;31m=====>item:\033[0m', item
                   yield item
                if self.page>=40:
                   print "循环解析结束,解析40页"
                   self.page=1
                   return

                next_page_url = response._url.replace(".html","") +"_p_"+str(self.page) + ".html"
                print "\033[1;31m[===next_page_url===]\033[0m:",next_page_url
                yield scrapy.Request(next_page_url,callback=self.parse)
            else:
                print '响应失败'