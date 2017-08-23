#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：Python的SQL操作模板类面向对象
  改进说明：接口泛化
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import MySQLdb
import json
import urllib2
import time
from datetime import date,datetime, timedelta

#########################  面向对象 Methods ##################################
class SQLTemlClass:
    def __init__(self):
        self.__conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='study')
        self.__cursor = self.__conn.cursor()  # cursorclass=MySQLdb.cursors.DictCursor
        self.__cursor.execute('set names utf8')

    def __del__(self):
        self.__cursor.close()
        self.__conn.close()

    def parse(self):
        sql="select * from datatype1 where name_char='hh';"
        try:
            self.__cursor.execute(sql)
            rows=self.__cursor.fetchall()
            if rows is None or not rows:
                print "not find"
                return
            for row in rows:
                print row
        except Exception,e:
            print str(e)


# 测试入口
if __name__ == "__main__":
    csql=SQLTemlClass()
    csql.parse()

