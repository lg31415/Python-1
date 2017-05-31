# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''
    添加要提取的属性
'''

# 南邮新闻页
class NanuNewsItem(scrapy.Item):
    news_title = scrapy.Field()    # 南邮新闻标题
    news_date = scrapy.Field()     # 南邮新闻时间
    news_url = scrapy.Field()      # 南邮新闻的详细链接


# xmp电影列表页
class XmpMovieItem(scrapy.Item):
    movie_title = scrapy.Field()    # 电影标题
    movie_url = scrapy.Field()      # 电影链接
    movie_score = scrapy.Field()    # 电影评分

# tudou系列验证
class TudouItem(scrapy.Item):
    item_title = scrapy.Field()    # 电影标题
    item_url = scrapy.Field()      # 电影链接
    item_jishu = scrapy.Field()    # 电影集数

