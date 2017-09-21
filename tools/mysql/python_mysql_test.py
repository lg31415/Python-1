#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:python-mysql测试
    Ref:
    State：
    Date:2017/6/15
    Author:tuling56
'''
import re, os, sys
import hues
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

curdir=os.getcwd()
datapath=curdir.replace('/bin','/data')


# 测试python-mysql
def pymsql_test():
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='study') #新建的数据库
        cur=conn.cursor() #cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute('set names utf8')
    except Exception,e:
        print('open %s db fail'%("study"))
        sys.exit()

    #sql="select name_char,datetimetype from datatype where datetimetype<from_unixtime(%s)" %(1497521947)
    sql="select name_char from datatype where name_varchar='zhangwewr'"
    print sql
    cur.execute(sql)
    rows=cur.fetchall()
    print rows
    for row in rows:
        print row


# 测试入口
if __name__ == "__main__":
    pymsql_test()

