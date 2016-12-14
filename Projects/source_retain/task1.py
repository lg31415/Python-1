#-*coding:utf8-*-#
#__author__ = 'yjm

import pymysql
import csv
import time
import datetime

#part1 将本地文件导入数据库
'''
with open('E:\\SQL\\test\\xmp_28days_peerid.20150701','rb') as csvfile:
    reader3=csv.reader(csvfile)
    for row in reader3:
        print(row)
'''


# part2 数据库创建
try:
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='root',charaset='utf8')
    cur = conn.cursor()
    cur.execute('create database if not exists peerid_db character set utf8')
    conn.select_db('peerid_db')
    cur.execute('create table if not exists xmp_days_peerid(peerid varchar(20) not null,sta_date varchar(20),sta_source varchar(100),sta_version varchar(20)) character set utf8')
    cur.execute("create table if not EXISTS xmp_days_source(sta_date varchar(20),sta_source VARCHAR (20),install_num SMALLINT) character set utf8 ")
    #cur.execute('alter table xmp_days_peerid change sta_date sta_date varchar(20)')

    # 数据写入
    f = open("E:\\SQL\\test\\xmp_28days_peerid.20150701")
    for line in f.readlines():
        one_record = line.strip().split()
        print one_record
        #print 'peerid: %s date: %s source: %s version: %s' % one_record
        #字符串转日期
        #temp=time.strptime(one_record[1], '%Y%m%d')
        #m_date=datetime.date(temp[0],temp[1],temp[2])
        #m_date=one_record[1]
        #m_peeid=one_record[0]
        #m_source=one_record[2]
        #m_version=one_record[3]
        #cur.execute('insert into xmp_days_peerid values(one_record[0],date_time,one_record[2],one_record[3])')
        if len(one_record)==4:
            #peerid,date,source,version
            cur.execute("insert into xmp_days_peerid(peerid,sta_date,sta_source,sta_version) values (%s,%s,%s,%s)",one_record)
    f.close()


    #先按天分，再按来源分
    sql="select datetime.date(time.strptime(sta_date,'%Y%m%d')),sta_source,count(*) as gpnum from xmp_days_peerid GROUP by datetime.date(time.strptime(sta_date,'%Y%m%d')),sta_source"


    cur.execute('select * from xmp_days_peerid')
    #数据统计
    source_list=[]
    source=open('source_list.txt','r')
    for line in source.readlines():
        line=line.strip()
        source_list.append(line)
    print source_list

    source_statics={}
    for r in cur.fetchall():
        if r[2] in source_list:
            #print(r[2])
            try:
                source_statics[r[2]]=source_statics.get(r[2],0)+1;
            except ValueError:
                pass
        else:
            #print("don't care source" )
            pass
        # print(type(r))  # return tuple
    print(source_statics)

    #数据入库
    for source in source_list:
        if source_statics.get(source):
            sql="insert into xmp_days_source(sta_date,sta_source,install_num) values('ha',%s,%d)" % (repr(source),source_statics[source])
            cur.execute(sql)
        else:
            pass
            #sql="insert into xmp_days_source(sta_date,sta_source,install_num) values('ha',%s,%d)" % (repr(source),0)
            #print sql
            #cur.execute(sql)

    conn.commit() # 提交事务
    cur.close()
    conn.close()
except pymysql.Error, e:
    print("mysql error %d:%s" %(e.args[0],e.args[1]))


