# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''
    添加要提取的属性
'''
class MyfirstscrapyItem(scrapy.Item):
    news_title = scrapy.Field()    # 南邮新闻标题
    news_date = scrapy.Field()     # 南邮新闻时间
    news_url = scrapy.Field()      # 南邮新闻的详细链接


