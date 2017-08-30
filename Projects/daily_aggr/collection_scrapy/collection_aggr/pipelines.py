# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import hashlib
import MySQLdb
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


class CollectionAggrPipeline(object):
    def __init__(self):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'root', db = 'media_lib')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
    
    def __del__(slef):
        self.cursor.close()
        self.conn.close()
    
    def process_item(self, item, spider):
        hues.log("==============Enter pipeline process_item()=====================")
        pageurl = self.transcode(item['pageurl'])
        m_md5 = hashlib.md5()
        m_md5.update(pageurl)
        pageurlhash = self.transcode(m_md5.hexdigest()) 

        # title
        title=item['title']
        # type
        type=item['type']
        # source
        source=item['source']
        # abstract
        abstract=item['abstract']
        # tags
        tags=item['tags']
        # publish_time
        publish_time=item['publish_time']


        ###进入逻辑判断环境
        sql="select count(*) from collection_base_info where pageurlhash='%s'" %(pageurlhash)
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        res_num=res[0][0]
        if not res_num:
            res_num=0

        if res_num==0:
            hues.info("数据库中无此资源")
            sql="replace into collection_base_info(pageurl,pageurlhash,title,type,source,abstract,tags,publish_time,insert_time)"
            paras=(pageurl,pageurlhash,title,type,source,abstract,tags,publish_time,'now()')
            m=self.cursor.execute(sql,paras)
            print '---->replace into collection_base_info:',title,"------>ret = ",m
        else:
            hues.info("数据库中已存在此资源")

        hues.log("==============Leave pipeline process_item()=====================")
        return item

    def transcode(self, content):
        content = MySQLdb.escape_string(content)
        return content