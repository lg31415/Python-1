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
    爬虫主体：负责处理请响应内容及url，处理完后交给pipline
'''
class XmpMoiveSpider(scrapy.Spider):
	name = "xmp_movie_list"
	allowed_domains = ["v.xunlei.com"]
	start_urls = [ "http://list.v.xunlei.com/v,type/5,movie/",]

	# 主解析函数
	def parse(self, response):
		page_num = 4
		news_page_num = 30
		if response.status == 200:
			for i in range(2,page_num+1):
				for j in range(1,news_page_num+1):
					item = XmpMovieItem()	    # 导入item
					target=response.xpath("/html/body/div[2]/ul")
					item['movie_title']=target.xpath("li["+str(j)+"]//p/a/text()").extract()[0]
					item['movie_url']=target.xpath("li["+str(j)+"]//p/a/@href").extract()[0]
					item['movie_score'] =target.xpath("li["+str(j)+"]//p/span[2]").xpath('string(.)').extract()[0]

					print '\033[1;31m=====>item:\033[0m',item
					yield item  #通过yield item来将存储下来的item交由后续的pipelines处理

				next_page_url = "http://list.v.xunlei.com/v,type/5,movie/page"+str(i)+"/"   # 之后通过生成next_page_url来通过scrapy.Request抓取下一页的新闻信息
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
