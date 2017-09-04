#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:elasticsearch的python接口
    Ref:http://www.cnblogs.com/yxpblog/p/5141738.html
    Date:2016/9/8
    Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


from datetime import datetime
from elasticsearch import Elasticsearch

#连接elasticsearch,默认是9200
es = Elasticsearch()

'''
    基本使用：创建索引和查询
'''
def basic_use():
    global res, hit
    ####### 创建索引，索引的名字是my-index,如果已经存在了，就返回个400，这个索引可以现在创建，也可以在后面插入数据的时候再临时创建
    es.indices.create(index='my-index', ignore=400)    #{u'acknowledged':True}

    #######插入数据,(这里省略插入其他两条数据，后面用)
    es.index(index="my-index", doc_type="test-type", id=01, body={"name": "中国共产党", "timestamp": datetime.now()})
    #{u'_type':u'test-type',u'created':True,u'_shards':{u'successful':1,u'failed':0,u'total':2},u'_version':1,u'_index':u'my-index',u'_id':u'1}
    #也可以，在插入数据的时候再创建索引test-index
    es.index(index="test-index", doc_type="test-type", id=42, body={"name": "共产主义", "timestamp": datetime.now()})

    #####查询数据，两种get and search
    #get获取【直接在URL中体现】
    res = es.get(index="my-index", doc_type="test-type", id=01)
    print(res)     #{u'_type': u'test-type', u'_source': {u'timestamp': u'2016-01-20T10:53:36.997000', u'any': u'data01'}, u'_index': u'my-index', u'_version': 1, u'found': True, u'_id': u'1'}
    print(res['_source'])    #{u'timestamp': u'2016-01-20T10:53:36.997000', u'any': u'data01'}

    #search获取【DSL方式】
    res = es.search(index="test-index", body={'query': {'match': {'any': 'data'}}})  #获取any字段=data的所有值
    print(res)

    res = es.search(index="test-index", body={"query": {"match_all": {}}})  #获取所有数据
    print(res)
    #{u'hits':
    #    {
    #    u'hits': [
    #        {u'_score': 1.0, u'_type': u'test-type', u'_id': u'2', u'_source': {u'timestamp': u'2016-01-20T10:53:58.562000', u'any': u'data02'}, u'_index': u'my-index'},
    #        {u'_score': 1.0, u'_type': u'test-type', u'_id': u'1', u'_source': {u'timestamp': u'2016-01-20T10:53:36.997000', u'any': u'data01'}, u'_index': u'my-index'},
    #        {u'_score': 1.0, u'_type': u'test-type', u'_id': u'3', u'_source': {u'timestamp': u'2016-01-20T11:09:19.403000', u'any': u'data033'}, u'_index': u'my-index'}
    #    ],
    #    u'total': 5,
    #    u'max_score': 1.0
    #    },
    #u'_shards': {u'successful': 5, u'failed': 0, u'total':5},
    #u'took': 1,
    #u'timed_out': False
    #}
    for hit in res['hits']['hits']:
        print(hit["_source"])


'''
    高级查询
'''
def medium_use():
    print "待和mongodb进行整合后实现"
    pass


# 测试入口
if __name__=="__main__":
    basic_use()
    medium_use()


