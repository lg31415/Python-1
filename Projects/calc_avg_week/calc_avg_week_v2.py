#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
  功能注释：计算（1,3,7,14,28，周留存）的一周平均值
'''

import os
import  sys
import  time
import  MySQLdb
from datetime import date,datetime,timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

#参数检查
def checkargs(stadate,tblname):
    #时间参数检查
    curdate=date.today()-timedelta(days=1)
    #curdate = '%04d%02d%02d' %(stadate.year, stadate.month, stadate.day)
    curtime=time.mktime(curdate.timetuple())
    statime=time.mktime(time.strptime(stadate,'%Y%m%d')) #将stadate转换成时间元组
    if(int(curtime)<int(statime)):
        print("Please check your input date")
        exit()

    #表名检查
    tbllists=('xmp_alive_online_source_percent',
              'xmp_alive_online_version_percent',
              'xmp_alive_push_source_percent',
              'xmp_alive_play_version_percent',
              'xmp_alive_play_source_percent')
    if tblname not in tbllists:
        print("Please check your input tablename")
        exit()


#结果计算
def calc_avg_week(cur,stadate_str,tblname):
    ##有数据的日期
    #当日留存（更早之前已有）
    yesdate=date.today()-timedelta(days=1)
    yesdate_str = '%04d%02d%02d' %(yesdate.year, yesdate.month, yesdate.day)

    #1日留存的最晚（更早之前以有）
    yesdate1=date.today()-timedelta(days=2)
    yesdate1_str = '%04d%02d%02d' %(yesdate1.year, yesdate1.month, yesdate1.day)

    #3日留存的最晚（更早之前已有）
    yesdate3=date.today()-timedelta(days=4)
    yesdate3_str = '%04d%02d%02d' %(yesdate3.year, yesdate3.month, yesdate1.day)

    #7日留存的最晚（更早之前已有）
    yesdate7=date.today()-timedelta(days=8)
    yesdate7_str = '%04d%02d%02d' %(yesdate7.year, yesdate7.month, yesdate7.day)

    #14日留存的最晚（更早之前已有）
    yesdate14=date.today()-timedelta(days=15)
    yesdate14_str = '%04d%02d%02d' %(yesdate14.year, yesdate14.month, yesdate14.day)

    #28日留存的最晚（更早之前已有）
    yesdate28=date.today()-timedelta(days=29)
    yesdate28_str = '%04d%02d%02d' %(yesdate28.year, yesdate28.month, yesdate28.day)

    #统计日期
    stadate_struct=time.strptime(stadate,'%Y%m%d')  #time.struct_time
    stadate_date=date(stadate_struct.tm_year,stadate_struct.tm_mon,stadate_struct.tm_mday)  #datetime.date
    #startdate=time.strftime('%Y%m%d',stadate_date.timetuple())            #20150922


    #1日留存的开始和结束日期
    if(stadate_str==yesdate_str):
        startdate1=stadate_date-timedelta(days=8)
        enddate1=stadate_date-timedelta(days=1)                           #datetime.date
    else:
        startdate1=stadate_date-timedelta(days=7)
        enddate1=yesdate
    startdate1=time.strftime('%Y%m%d',startdate1.timetuple())
    enddate1=time.strftime('%Y%m%d',enddate1.timetuple())

    #3日留存的开始和结束日期
    if(stadate_str<yesdate3_str):
        startdate3=stadate_date-timedelta(days=7)                           #datetime.date
    startdate=time.strftime('%Y%m%d',startdate3.timetuple())
    enddate3=stadate_date-timedelta(days=7)                           #datetime.date
    enddate3=time.strftime('%Y%m%d',startdate3.timetuple())

    #7日和周留存的开始和结束日期
    startdate7=stadate_date-timedelta(days=7)                           #datetime.date
    startdate7=time.strftime('%Y%m%d',startdate7.timetuple())
    enddate7=stadate_date-timedelta(days=7)                           #datetime.date
    enddate7=time.strftime('%Y%m%d',startdate7.timetuple())

    #14日留存的开始和结束日期
    startdate14=stadate_date-timedelta(days=7)                           #datetime.date
    startdate14=time.strftime('%Y%m%d',startdate14.timetuple())
    enddate14=stadate_date-timedelta(days=7)                           #datetime.date
    enddate14=time.strftime('%Y%m%d',startdate14.timetuple())

    #28日留存的开始和结束日期
    startdate28=stadate_date-timedelta(days=7)                           #datetime.date
    startdate28=time.strftime('%Y%m%d',startdate.timetuple())
    enddate28=stadate_date-timedelta(days=7)                           #datetime.date
    enddate28=time.strftime('%Y%m%d',startdate.timetuple())


    sql="select concat('%s','~','%s') as 统计日期,a.source as 安装渠道,\
        concat(avg(if(length(a.data1)!=0,convert(a.data1,decimal(6,4)),NULL)),'%%') as 1日留存均值,\
        concat(avg(if(length(a.data3)!=0,convert(a.data3,decimal(6,4)),NULL)),'%%') as 3日留存均值,\
        concat(avg(if(length(a.data7)!=0,convert(a.data7,decimal(6,4)),NULL)),'%%') as 7日留存均值,\
        concat(avg(if(length(a.data14)!=0,convert(a.data14,decimal(6,4)),NULL)),'%%') as 14日留存均值,\
        concat(avg(if(length(a.data28)!=0,convert(a.data28,decimal(6,4)),NULL)),'%%') as 28日留存均值,\
        concat(avg(if(length(a.last_week)!=0,convert(a.last_week,decimal(6,4)),NULL)),'%%') as 周留存均值\
        from %s as a inner join xmp_install_source_total b  on b.source=a.source where a.date=b.date and\
        a.date>'%s' and a.date<='%s' \
        group by a.source" %(startdate,stadate,tblname,startdate,stadate)
    print '[sql]\n',sql
    #cur.execute(sql)
    #将查询结果输出到文件中
    cmd='''mysql -uroot -phive -e "set names utf8;use pgv_stat;%s">%s'''  %(sql,tblname+'.txt')
    print '[cmd]\n',cmd
    os.system(cmd)

if __name__ == "__main__":
    ##参数检查
    if len(sys.argv)<2:
        stadate=date.today()-timedelta(days=1)
        stadate = '%04d%02d%02d' %(stadate.year, stadate.month, stadate.day)
        tblname='xmp_alive_online_source_percent'   #默认上线留存按渠道
	print '[stadata]',stadate,'\n','[tblname]',tblname
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


