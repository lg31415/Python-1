#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:练手项目：片库电影页爬虫
	Ref:
	State：
	Date:2017/5/24
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy
from myfirstscrapy.items import XmpMovieItem


'''
    基础版：
    存在着重复抓取的问题
'''
class XmpMoiveSpiderBase(scrapy.Spider):
	name = "xmp_movie_list"
	allowed_domains = ["v.xunlei.com"]
	start_urls = [ "http://list.v.xunlei.com/v,type/5,movie/",]
	def __init__(self):
		self.page=0

	# 主解析函数
	def parse(self, response):
		self.page=self.page+1
		print "第%s次进入parse回掉函数" %(str(self.page))
		page_num = 3
		news_page_num = 4
		if response.status == 200:
			for i in range(2,page_num+1):
				print "====curi:",i,"range:",range(2,page_num+1)
				for j in range(1,news_page_num+1):
					item = XmpMovieItem()	    # 导入item
					target=response.xpath("/html/body/div[2]/ul")
					item['movie_title']=target.xpath("li["+str(j)+"]//p/a/text()").extract()[0]
					item['movie_url']=target.xpath("li["+str(j)+"]//p/a/@href").extract()[0]
					item['movie_score'] =target.xpath("li["+str(j)+"]//p/span[2]").xpath('string(.)').extract()[0]
					#print '\033[1;31m=====>item:\033[0m',item
					yield item  #通过yield item来将存储下来的item交由后续的pipelines处理

				# 通过在请求体中使用yield
				next_page_url = "http://list.v.xunlei.com/v,type/5,movie/page"+str(i)+"/"   # 之后通过生成next_page_url来通过scrapy.Request抓取下一页的新闻信息
				print "\033[1;31m[===next_page_url===]\033[0m:",next_page_url
				yield scrapy.Request(next_page_url,callback=self.parse_news)				# 通过Request请求来达到连续处理的效果
		else:
			print "响应失败"


	# 回调函数（和主解析函数很相似，可以合并为一）
	def parse_news(self, response):
		news_page_num = 14
		if response.status == 200:
			for j in range(1,news_page_num+1):
				item = XmpMovieItem()
				target=response.xpath("/html/body/div[2]/ul")
				item['movie_title']=target.xpath("li["+str(j)+"]//p/a/text()").extract()[0]
				item['movie_url']=target.xpath("li["+str(j)+"]//p/a/@href").extract()[0]
				item['movie_score'] =target.xpath("li["+str(j)+"]//p/span[2]/b/text()").extract()[0]

				yield item  #通过yield item来将存储下来的item交由后续的pipelines处理


'''
	增强版1：修复重复抓取的问题
	通过start_urls列表实现
'''
class XmpMoiveSpiderImpl1(scrapy.Spider):
	name = "xmp_movie_list_impl1"
	allowed_domains = ["v.xunlei.com"]
	start_urls = [ "http://list.v.xunlei.com/v,type/5,movie/",]
	start_urls.extend(["http://list.v.xunlei.com/v,type/5,movie/page{num}/".format(num=num) for num in range(2,4)])

	# 主解析函数
	def parse(self, response):
		news_page_num = 4
		if response.status == 200:
			for j in range(1,news_page_num+1):
				item = XmpMovieItem()
				target=response.xpath("/html/body/div[2]/ul")
				item['movie_title']=target.xpath("li["+str(j)+"]//p/a/text()").extract()[0]
				item['movie_url']=target.xpath("li["+str(j)+"]//p/a/@href").extract()[0]
				item['movie_score'] =target.xpath("li["+str(j)+"]//p/span[2]").xpath('string(.)').extract()[0]
				#print '\033[1;31m=====>item:\033[0m',item
				yield item
		else:
			print "响应失败"


'''
    增强版2：解决了重复抓取的问题
    利用类变量控制回调函数的次数达到抓取指定数量的页面的目的
'''
class XmpMoiveSpiderImpl2(scrapy.Spider):
    name = "xmp_movie_list_impl2"
    allowed_domains = ["v.xunlei.com"]
    start_urls = ["http://list.v.xunlei.com/v,type/5,movie/",]

    def __init__(self):
        self.page=1

    # 主解析函数
    def parse(self, response):
        self.page=self.page+1
        news_page_num = 4
        if response.status == 200:
            for j in range(1, news_page_num + 1):
                item = XmpMovieItem()
                target = response.xpath("/html/body/div[2]/ul")
                item['movie_title'] = target.xpath("li[" + str(j) + "]//p/a/text()").extract()[0]
                #item['movie_url'] = target.xpath("li[" + str(j) + "]//p/a/@href").extract()[0]
                #item['movie_score'] = target.xpath("li[" + str(j) + "]//p/span[2]").xpath('string(.)').extract()[0]
                #print '\033[1;31m=====>item:\033[0m', item
                yield item
            if self.page>5:	# 注意这个判断不能否在yield scrapy.Request之后，不然循环永远不会终止
                print "循环解析结束"
                return
            next_page_url = "http://list.v.xunlei.com/v,type/5,movie/page" + str(self.page) + "/"
            print "\033[1;31m[===next_page_url===]\033[0m:",next_page_url
            yield scrapy.Request(next_page_url,callback=self.parse)
        else:
            print "响应失败"
