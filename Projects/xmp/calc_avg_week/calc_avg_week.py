#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：计算（1,3,7,14,28，周留存）的一周平均值
'''

import os
import  sys
import  time
import  MySQLdb
from datetime import date,datetime,timedelta

#参数检查
def checkargs(stadate,tblname):
    #时间参数检查
    curdate=date.today()-timedelta(days=1)
    #curdate = '%04d%02d%02d' %(curdate.year, curdate.month, curdate.day)  #datetime.date类型转换成20150922这种字符形式，方式一
    #curdate=date.strftime(curdate,'%Y%m%d')                               #datetime.date类型转换成20150922这种字符形式，方式二
    curtime=time.mktime(curdate.timetuple())             #将当前日期转换成时间戳
    statime=time.mktime(time.strptime(stadate,'%Y%m%d')) #将stadate转换成时间戳

    if(int(curtime)<int(statime)):
        print("Please check the your input date")
        exit()

    #表名检查
    tbllists=('xmp_alive_online_source_percent',
              'xmp_alive_online_version_percent',
              'xmp_alive_push_source_percent',
              'xmp_alive_play_version_percent',
              'xmp_alive_play_source_percent')
    if tblname not in tbllists:
        print("Please check your input table name")
        exit()


#结果计算
def calc_avg_week(cur,stadate,tblname):
    #统计的开始日期
    stadate=time.strptime(stadate,'%Y%m%d')  #time.struct_time
    stadate_temp=date(stadate.tm_year,stadate.tm_mon,stadate.tm_mday)  #datetime.date
    startdate=stadate_temp-timedelta(days=7)                           #datetime.date
    startdate=time.strftime('%Y%m%d',startdate.timetuple())            #datetime.date-->time.struct_time

    sql="select %s as 日期,a.source as 安装渠道,\
        concat(avg(if(length(a.data1)!=0,convert(a.data1,signed),'')),'%') as 1日留存,\
        concat(avg(if(length(a.data3)!=0,convert(a.data3,signed),'')),'%') as 3日留存,\
        concat(avg(if(length(a.data7)!=0,convert(a.data7,signed),'')),'%') as 7日留存,\
        concat(avg(if(length(a.data14)!=0,convert(a.data14,signed),'')),'%') as 14日留存,\
        concat(avg(if(length(a.data28)!=0,convert(a.data28,signed),'')),'%') as 28日留存, \
        concat(avg(if(length(a.last_week)!=0,convert(a.last_week,signed),'')),'%') as 周留存\
        from %s as a inner join xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' group by a.source" %(stadate,tblname,stadate)
    print '[sql]\n',sql
    cur.execute(sql)
    #将查询结果输出到文件中
    cmd="mysql -uroot -phive -e '%s'>%s" %(sql,tblname+'.txt')
    os.system(cmd)

if __name__ == "__main__":
    ##参数检查
    if len(sys.argv)<2:
        stadate=date.today()-timedelta(days=1)
        stadate = '%04d%02d%02d' %(stadate.year, stadate.month, stadate.day) #统计日期
        tblname='xmp_alive_online_source_percent'   #默认上线留存按渠道
    else:
        stadate=sys.argv[1]
        tblname=sys.argv[2]
    checkargs(stadate,tblname)
    ## 建立连接
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='hive',db='pgv_stat') #新建的数据库
    if not conn.open:
        print('open %s db fail'%('pgv_stat'))
        exit()
    cur=conn.cursor()
    cur.execute('set names utf8')

    ##计算
    calc_avg_week(cur,stadate,tblname)

    ##关闭连接
    cur.close()
    conn.close()





