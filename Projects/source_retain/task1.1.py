# -*-coding:utf-8-*-
#__author__ = 'yjm
'''
 Problem:本地文本文件导入到数据库的时候，提示load data local infile is not allowed;
 解决方法：采用cmd执行的方式，注意命令格式的设置
 功能：计算一天某个渠道的留存

'''

import pymysql
import os

# part1 数据库和表创建及数据导入
try:
    #数据库和表创建
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root')
    cur = conn.cursor()
    cur.execute('create database if not exists peerid_db character set utf8')
    conn.select_db('peerid_db')
    cur.execute(
        'create table if not exists xmp_days_peerid(peerid varchar(20) not null,sta_date varchar(20),sta_source varchar(20),sta_version varchar(20)) character set utf8')
    cur.execute(
        "create table if not EXISTS xmp_days_source(sta_date varchar(20),sta_source VARCHAR (20),install_num INT) character set utf8 ")
    #cur.execute('alter table xmp_days_peerid change sta_date sta_date varchar(20)')~

    # 数据导入
    print('load data to table......')
    #method1
    # sql = "load data local infile 'E:\\SQL\\test\\xmp_28days_peerid.20150701' into table peerid_db.xmp_days_peerid1(peerid,sta_date,sta_source,sta_version)"
    # cur.execute(sql)
    # conn.commit()
    #method2
    cmd='''mysql -uroot -proot peerid_db --local-infile=1 \
          -e "load data local infile 'E://SQL//test//sub_data.txt' \
          into table xmp_days_peerid(peerid,sta_date,sta_source,sta_version)"
        '''
    #print(cmd)
    os.system(cmd)
    print('load data sucessfully')

except pymysql.Error, e:
    print("mysql error %d:%s" % (e.args[0], e.args[1]))


#Part2 数据统计，先按天统计,然后按来源分
#安装源
source_list=[]
source=open('source_list.txt','r')
for line in source.readlines():
    line=line.strip()
    source_list.append(line)
source_list=str(tuple(source_list))

try:
    sql='select sta_date,sta_source,count(*) from xmp_days_peerid where sta_source in %s group by sta_date,sta_source ' %(source_list)
    #print(sql)
    cur.execute(sql)
    dayresults = cur.fetchall()
    conn.commit()

    #数据入库
    sql = cur.executemany("insert into xmp_days_source(sta_date,sta_source,install_num) VALUES ('%s','%s','%s')",dayresults)
    conn.commit()
    cur.close()
    conn.close()
except Exception, e:
    print("ERROR", e)


