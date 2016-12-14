#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：sqllite3嵌入式关系数据库,其数据库就是一个文件
'''

import sqlite3

def msqlite3():
    conn=sqlite3.connect('sqllite3_test.db')
    cursor = conn.cursor()
    #cursor.execute('create table if NOT EXISTS user (id varchar(20) primary key, name varchar(20))')
    cursor.execute('insert into user (id, name) values (\'2\', \'zhang\')')
    print cursor.rowcount
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    msqlite3()
