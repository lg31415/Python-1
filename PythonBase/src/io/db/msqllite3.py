#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
    功能注释：sqllite3嵌入式关系数据库,其数据库就是一个文件
    参考：http://www.runoob.com/sqlite/sqlite-tutorial.html
'''

import sqlite3

class CSqlite3():
    def __init__(self):
        self.conn=sqlite3.connect('sqllite3.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def dcl(self):
        csql="create table if not exists baseinfo(id int auto_increment primary key, name varchar(20),age smallint,insert_time datetime);"
        self.cursor.execute(csql)

    def dml(self):
        insql="insert into baseinfo(name, age,insert_time) values ('张小二',12,datetime())"
        self.cursor.execute(insql)
        print self.cursor.rowcount

# 测试入口
if __name__ == "__main__":
    msql3=CSqlite3()
    msql3.dcl()
    msql3.dml()
