# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
    爬虫数据的后续处理
    管道的类名是否要和items定义的要爬取的字段名相同？？？
'''

import MySQLdb
import hues
import json

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

# 管道3:土豆处理
class TudouAllPipeline(object):
    def __init__(self,ctype='all'):
        self.file = open('tudou_all.txt',mode='wb')

    # 打开蜘蛛的时候执行
    def open_spider(self, spider):
        hues.info("TudouAllPipeline蜘蛛打开")

    # 关闭蜘蛛的时候执行
    def close_spider(self,spider):
        hues.info("TudouAllPipeline蜘蛛关闭")

    def process_item(self, item, spider):
        self.file.write(item['item_title'].encode("utf8"))
        self.file.write("\n")
        self.file.write(item['item_url'].encode("utf8"))
        self.file.write("\n")
        self.file.write(item['item_jishu'].encode("utf8"))
        self.file.write("\n")
        #hues.success(json.dumps(item,ensure_ascii=False))
        return item
        
# 管道3:qqrecomm处理,存入关系库
class QQrecommPipeline(object):
    def __init__(self):
        self.__conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='study')
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute('set names utf8')
        self.__id_mapping={}

    def __del__(self):
        self.__cursor.close()
        self.__conn.close()

    def __addrecord2craw(self,pageurl):
        sql="insert into url_to_crawled values()"

    # 新的推荐关系插入
    def tuple_list_to_db(self,tuple_list):
        mutisql="replace into qq_relation_info values ('%s','%s','NOW()','NOW()')"
        self.__cursor.executemany(mutisql,tuple_list)

    # 根据pageurl查询movieid
    def url2moieid(self,pageurl):
        pageurlhash=pageurl  # md5
        sql="select pageurl,dealt_flag from third_party_base_info where pageurlhash='%s';" %(pageurlhash)
        self.__cursor.execute(sql)
        rows=self.__cursor.fetchall()
        if rows is None or not rows:
            hues.warn('%s has never been crawled' %(pageurl))
            self.__addrecord2craw(pageurl)
            return ''
        if len(rows)==1:
            pageurl,dealt_flag=rows[0]
            if dealt_flag==1:
                hues.info('%s to be matched' %(pageurl))
                return ''
            sql="select movieid from id_mapping where odl_id='%s'" %(pageurlhash)
            self.__cursor.execute(sql)
            rows=self.__cursor.fetchall()
            movieid=rows[0][0]
            return movieid

    def process_item(self, item, spider):
        relations=[]
        pageurl=item['item_url']
        movieid=self.url2moieid(pageurl)
        recomm_pageurls=item['item_recomurls']
        for url in recomm_pageurls:
            recomm_movieid=self.url2moieid(url)
            if movieid and recomm_movieid:
                relations.append((movieid,recomm_movieid))
            else:
                hues.warn('pageurl not has never been crawled:%s' %(url))
        self.tuple_list_to_db(relations)
        return item