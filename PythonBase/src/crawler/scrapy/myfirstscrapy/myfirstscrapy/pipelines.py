# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
    爬虫数据的后续处理
    管道的类名是否要和items定义的要爬取的字段名相同？？？
'''

# 管道1：南邮新闻页处理
class NanuNewsPipeline(object):
    def __init__(self):
        self.file = open('njupt.txt',mode='wb')
    def process_item(self, item, spider):
        self.file.write(item['news_title'].encode("utf8"))
        self.file.write("\n")
        self.file.write(item['news_date'].encode("utf8"))
        self.file.write("\n")
        self.file.write(item['news_url'].encode("utf8"))
        self.file.write("\n")
        return item

# 管道2:xmp电影页处理
class XmpMoviePipeline(object):
    def __init__(self):
        self.file = open('xmp_movie.txt',mode='wb')
    def process_item(self, item, spider):
        self.file.write(item['movie_title'].encode("utf8"))
        self.file.write("\n")
        self.file.write(item['movie_url'].encode("utf8"))
        self.file.write("\n")
        self.file.write(item['movie_score'].encode("utf8"))
        self.file.write("\n")
        return item