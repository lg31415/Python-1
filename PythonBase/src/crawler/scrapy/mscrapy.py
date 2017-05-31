#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：scrapy模块学习
  参考网址: http://python.jobbole.com/85281/
'''

from scrapy.selector import HtmlXPathSelector

def parse(self,response):
    hxs=HtmlXPathSelector(response)
    hxs.select('//a/@href').extract()

    sites=['site1','site2']
    for site in sites:
        item ={}
        item['title'] = site.select('a/text()').extract()
        item['link'] = site.select('a/@href').extract()
        item['desc'] = site.select('text()').extract()


# 测试入口
if __name__ == "__main__":
    parse()
