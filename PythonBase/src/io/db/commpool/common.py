#!/bin/env python
#coding:utf-8

import types
import MySQLdb
import connect_db
import sys
import time
import datetime

test_db_host = "localhost"
test_db_port = 3306

formal_db_host = "localhost"
formal_db_port = 3316


conn_map = {}

# 返回的是最后的列表结果
def execute_sql(sql, db_host = test_db_host, db_port = test_db_port, db_user = 'root', db_passwd = 'root', db_name = 'labs', conn_index = 1)
    conn_info = None
    conn_key = "%s%d%s%d"%(db_host, db_port, db_name, conn_index)
    conn_info = conn_map.get(conn_key)
    if conn_info == None:
        print "not have established yet,key:%s connect..."%(conn_key)
        conn_info = connect_db.connect_media_resource_db(db_host, db_port, db_user, db_passwd, db_name)
        conn_map[conn_key] = conn_info
    while True:
        try:
            cur = conn_info[1]
            conn = conn_info[0]
            cur.execute(sql)
            conn.commit()
            rows = cur.fetchall()
            return rows
        except _mysql_exceptions.OperationalError, e:
            print 'get failed with OperationalError: ' + str(e) + ", retry!"
            connect_db.close_media_resource_db_connect(conn_info)
            time.sleep(1)
            conn_info = connect_db.connect_media_resource_db(db_host, db_port, db_user, db_passwd, db_name)
            conn_map[conn_key] = conn_info





