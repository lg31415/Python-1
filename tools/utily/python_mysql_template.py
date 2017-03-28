#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：PythonSQL操作模板
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
from datetime import date,  datetime, timedelta

#########################  Methods ##################################
# 初始化工作，打开连接
def init_conn(db):
	## 建立连接
    try:
    	conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db=db) #新建的数据库
    	cur=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    	cur.execute('set names utf8')
    except Exception,e:
        print('open %s db fail'%(db))
 		exit()
 	return conn,cur

# 创建表
def create_tbl():
	sql = 'CREATE TABLE IF NOT EXISTS baseInfo(\
		id bigint(20) NOT NULL AUTO_INCREMENT,\
		videoID varchar(12) NOT NULL DEFAULT "",\
		title varchar(256) NOT NULL DEFAULT "",\
		type varchar(40) NOT NULL DEFAULT "",\
		subtype varchar(40) NOT NULL DEFAULT "",\
		year char(4) NOT NULL DEFAULT "",\
		style varchar(64) NOT NULL DEFAULT "",\
		source varchar(40) NOT NULL DEFAULT "",\
		quality varchar(512) NOT NULL DEFAULT "",\
		label varchar(256) NOT NULL DEFAULT "",\
		member varchar(64) NOT NULL DEFAULT "",\
		group_ varchar(64) NOT NULL DEFAULT "",\
		team varchar(64) NOT NULL DEFAULT "",\
		poster varchar(512) NOT NULL DEFAULT "",\
		vv int not NULL DEFAULT 0,\
		point varchar(1024) NOT NULL DEFAULT "",\
		subcnt int not NULL DEFAULT 0,\
		status_e int not NULL DEFAULT 0,\
		operater varchar(64) NOT NULL DEFAULT "",\
		insert_t datetime NOT NULL DEFAULT "0000-00-00 00:00:00",\
		update_t datetime NOT NULL DEFAULT "0000-00-00 00:00:00",\
		ts datetime NOT NULL DEFAULT "0000-00-00 00:00:00",\
		PRIMARY KEY (id),\
		UNIQUE KEY videoID (videoID),\
		KEY title (title)\
		) ENGINE=MyISAM DEFAULT CHARSET=utf8;'
	print sql
	cur.execute(sql)
	conn.commit()

# 数据插入
def insert_data():
	load_sql="load data local infile '%s' into table task1_tbl(s_key,t_time,vv);" %('redis_export.txt')  #fields terminated by '\t'
	#insert muti
	sql="insert into persons(Id_P,LastName) VALUES (%s,%s)"
    mutivals=((int(11),"zhag"),(int(12),"gaug"))
    cur.executemany(sql, mutivals)

    #insert single
    sql="insert into persons(Id_P,LastName) VALUES (%s,'%s')" % (16,'yjm')  #按转换类型插入,整型当成字符型输入
	cur.execute(sql)	

# 数据查询(一次性取完)
def select_all_data():
	#测试1
    sql="select Id_P,LastName from persons ORDER BY Id_P"
    try:
        cur.execute(sql)
    except Exception,e:
        print(e)
    alldata=cur.fetchall()
    print('type<fetchall>',type(alldata),alldata)
    if alldata: #读取到数据
        for rec in alldata:
            print(type(rec[0]),rec[0],type(rec[1]),rec[1])
    conn.commit()

    #测试2
    sql="select Id_P,LastName from persons ORDER BY Id_P"
    try:
        cur.execute(sql)
    except Exception,e:
        print(e)
    manydata=cur.fetchmany(3)
    print('type<fetchall>',type(manydata),manydata)
    if manydata: #读取到数据
        for rec in manydata:
            print(type(rec[0]),rec[0],type(rec[1]),rec[1])
    conn.commit()

    # 测试3（带字段名读取）(参考：http://python.jobbole.com/85589/)
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute("select * from persons limit 3")
    res=cur.fetchall()
    print res

# 数据查询(取单个数据)
def select_each_data():
	sql="use mjoin;select Id_P,LastName from persons ORDER BY Id_P"
    try:
        cur.execute(sql)
    except Exception,e:
        print(e)
    onedata=cur.fetchone()
    print('type<fetchall>',type(onedata),onedata)
    while onedata: #读取到数据
        for rec in onedata:
            print rec,
        print
        onedata=cur.fetchone()
    #conn.commit()


# 数据导入
def inport_data(conn,cur):
	load_sql="use db1;load data local infile '%s' into table db1.tb1 character set utf8 fields terminated by ',';"
	try:
        cur.execute(load_sql)
    except Exception,e:
        print(e)


# 数据导出(mysql)
def export_data(conn,cur):
	sql="select * from xmp_pianku_part where date='%s' order by date desc, part asc" %(stadate)
	cur.execute(sql)
    conn.commit()
    qresutls=cur.fetchall()
    
    # 导出成js对象的文本文件
    jsdata='var click_data='+str(list(qresutls));
    with open(datapath+'click_data.js','w') as f:
    	f.write(jsdata)	

# 数据导出(hive)
g_tool_hive="/usr/local/complat/complat_clients/cli_bin/hive"
def export_data_hive():
	hsql='%s -e "use xmp_odl; select c1,c2 from tbl where ds=%s and  install in (\"2408\",\"2608\",\"3088\")" > %s' % (g_tool_hive,yestoday,file_name)
	print hsql
    if os.system(hsql) != 0:
        print "get %s data from t_stat_url_upload_split failed" % (yestoday)
        exit()

# 关闭连接
def close_down(conn,cur):
	cur.close()
    conn.close()


###########################  Process Flow ##########################
if __name__ == "__main__":
    if len(sys.argv)<2:
        stadate='20150817' #raw_input('Please input the stadate:')
        #stadate=date.today()-timedelta(days=1)
        #stadate = '%04d%02d%02d' %(stadate.year, stadate.month, stadate.day)
    else:
        stadate=sys.argv[1]
   
 	readData()


