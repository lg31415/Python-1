#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:http://blog.csdn.net/caleng/article/details/5712850
	State：
	Date:2016/11/11
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import web
import datetime

'''
	use test;
	CREATE TABLE entries (    
    id INT AUTO_INCREMENT,    
    title TEXT,    
    content TEXT,    
    posted_on DATETIME,    
    primary key (id)    
);  
'''

#数据库连接
db = web.database(dbn = 'mysql', db = 'world', user = 'root', pw = 'root')

#获取所有文章
def get_posts():
    return db.select('entries', order = 'id DESC')

#获取文章内容
def get_post(id):
    try:
        return db.select('entries', where = 'id=$id', vars = locals())[0]
    except IndexError:
        return None

#新建文章
def new_post(title, text):
    db.insert('entries',
        title = title,
        content = text,
        posted_on = datetime.datetime.utcnow())

#删除文章
def del_post(id):
    db.delete('entries', where = 'id = $id', vars = locals())

#修改文章
def update_post(id, title, text):
    db.update('entries',
        where = 'id = $id',
        vars = locals(),
        title = title,
        content = text)
