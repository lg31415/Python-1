#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：redis数据库使用
  参考：http://www.cnblogs.com/melonjiang/p/5342505.html
'''

import redis

def mredis():
    r=redis.StrictRedis(host='localhost',port=6379)
    r.set('kkey1','vv1')
    print r.get('kkey1'),r['kkey1']
    print r.keys()
    print r.dbsize()
    r.save()
    r.flushdb()    #清空所有数据



if __name__ == "__main__":
    mredis()
