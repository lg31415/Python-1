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

#准备工作
#def create_mid_table(conn,cur):
#    sql='''use pgv_stat_mid;create table if not exists xmp_avg_week(sdate varchar(10),source varchar(10),
#           1dayavg varchar(10),3dayavg varchar(10),7dayavg varchar(10),14dayavg varchar(10),28dayavg varchar(10),weekavg varchar(10))
#           character set utf8;
#        '''
#    cur.execute(sql)
#    conn.commit()

#结果计算
def calc_avg_week(conn,cur,stadate,tblname):
    ##有数据的日期
    #当日留存（更早之前已有）
    yesdate=date.today()-timedelta(days=1)
    yesdate_str = '%04d%02d%02d' %(yesdate.year, yesdate.month, yesdate.day)
    #yesdate_str=time.strftime('%Y%m%d',yesdate.timetuple())        #20150922

    #统计日期
    stadate_struct=time.strptime(stadate,'%Y%m%d')  #time.struct_time
    stadate_date=date(stadate_struct.tm_year,stadate_struct.tm_mon,stadate_struct.tm_mday)  #datetime.date

 
    #1日留存的开始和结束日期
    enddate1=stadate_date-timedelta(days=1)
    startdate1=enddate1-timedelta(days=7)                          #datetime.date
    startdate1=time.strftime('%Y%m%d',startdate1.timetuple())
    enddate1=time.strftime('%Y%m%d',enddate1.timetuple())
    print '[startdate1-enddate1]:',startdate1,enddate1

    #3日留存的开始和结束日期
    enddate3=stadate_date-timedelta(days=3)
    startdate3=enddate3-timedelta(days=7)                          #datetime.date
    startdate3=time.strftime('%Y%m%d',startdate3.timetuple())
    enddate3=time.strftime('%Y%m%d',enddate3.timetuple())
    print '[startdate3-enddate3]:',startdate3,enddate3

    #7日留存的开始和结束日期
    enddate7=stadate_date-timedelta(days=7)
    startdate7=enddate7-timedelta(days=7)      
    startdate7=time.strftime('%Y%m%d',startdate7.timetuple())
    enddate7=time.strftime('%Y%m%d',enddate7.timetuple())
    print '[startdate7-enddate7]:',startdate7,enddate7

    #14留存的开始和结束日期
    enddate14=stadate_date-timedelta(days=14)
    startdate14=enddate14-timedelta(days=7)   
    startdate14=time.strftime('%Y%m%d',startdate14.timetuple())
    enddate14=time.strftime('%Y%m%d',enddate14.timetuple())
    print '[startdate14-enddate14]:',startdate14,enddate14

    #28日留存的开始和结束日期
    enddate28=stadate_date-timedelta(days=28)
    startdate28=enddate28-timedelta(days=7)   
    startdate28=time.strftime('%Y%m%d',startdate28.timetuple())
    enddate28=time.strftime('%Y%m%d',enddate28.timetuple())
    print '[startdate28-enddate28]:',startdate28,enddate28

    #计算部分
    sql="select %s as 统计日期,a.source as 安装渠道,concat(avg(if(length(a.data1)!=0,convert(a.data1,decimal(6,4)),NULL)),'%%') as 1日留存均值 from pgv_stat.%s as a inner join pgv_stat.xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate1,enddate1)
    print '[1sql]\n',sql
    cur.execute(sql)
    results=cur.fetchall()
    for item in results:
        sql="insert into pgv_stat_mid.xmp_week_avg(mdate,source,1dayavg) values('%s','%s','%s');" %(item[0],item[1],item[2])
        cur.execute(sql)
        conn.commit()

    sql="select %s as 统计日期,a.source as 安装渠道, concat(avg(if(length(a.data3)!=0,convert(a.data3,decimal(6,4)),NULL)),'%%') as 3日留存均值 from pgv_stat.%s as a inner join pgv_stat.xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate3,enddate3)
    print '[3sql]\n',sql
    cur.execute(sql)
    results=cur.fetchall()
    for item in results:
        sql="update pgv_stat_mid.xmp_week_avg set 3dayavg='%s' where source='%s';" %(item[2],item[1])
        cur.execute(sql)
        conn.commit()

    sql="select %s as 统计日期,a.source as 安装渠道,concat(avg(if(length(a.data7)!=0,convert(a.data7,decimal(6,4)),NULL)),'%%') as 7日留存均值 from pgv_stat.%s as a inner join pgv_stat.xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate7,enddate7)
    print '[7sql]\n',sql
    cur.execute(sql)
    results=cur.fetchall()
    for item in results:
        sql="update pgv_stat_mid.xmp_week_avg set 7dayavg='%s' where source='%s';" %(item[2],item[1])
        cur.execute(sql)
        conn.commit()

    sql="select %s as 统计日期,a.source as 安装渠道,concat(avg(if(length(a.data14)!=0,convert(a.data14,decimal(6,4)),NULL)),'%%') as 14日留存均值 from pgv_stat.%s as a inner join pgv_stat.xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate14,enddate14)
    print '[14sql]\n',sql
    cur.execute(sql)
    results=cur.fetchall()
    for item in results:
        sql="update pgv_stat_mid.xmp_week_avg set 14dayavg='%s' where source='%s';" %(item[2],item[1])
        cur.execute(sql)
        conn.commit()


    sql="select %s as 统计日期,a.source as 安装渠道,concat(avg(if(length(a.data28)!=0,convert(a.data28,decimal(6,4)),NULL)),'%%') as 28日留存均值 from pgv_stat.%s as a inner join pgv_stat.xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate28,enddate28)
    print '[28sql]\n',sql
    cur.execute(sql)
    results=cur.fetchall()
    for item in results:
        sql="update pgv_stat_mid.xmp_week_avg set 28dayavg='%s' where source='%s';" %(item[2],item[1])
        cur.execute(sql)
        conn.commit()

    #将查询结果输出到文件中
    sql='''set names utf8;select mdate as 统计日期,source as 安装渠道,concat(round(1dayavg,2),'%') as 1日留存均值, concat(round(3dayavg,2),'%') as 3日留存均值,concat(round(7dayavg,2),'%') as 7日留存均值,concat(round(14dayavg,2),'%') as 14日留存均值,concat(round(28dayavg,2),'%') as 28日留存均值,concat(round(7dayavg,2),'%') as 周留存均值 from pgv_stat_mid.xmp_week_avg;'''
    cmd='''mysql -uroot -phive -e "%s">%s''' %(sql,tblname+'.txt')
    print '[cmd]\n',cmd
    os.system(cmd)


if __name__ == "__main__":
    ##参数检查
    if len(sys.argv)<2:
        stadate=date.today()-timedelta(days=1)
        stadate = '%04d%02d%02d' %(stadate.year, stadate.month, stadate.day)
        tblname='xmp_alive_online_source_percent'   #默认上线留存按渠道
    else:
        stadate=sys.argv[1]
        tblname=sys.argv[2]
    print '[stadata]',stadate,'\n','[tblname]',tblname
    checkargs(stadate,tblname)
    
    ## 建立连接并初始化中间表
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='hive') #新建的数据库
    if not conn.open:
        print('open connnection fail')
        exit()
    cur=conn.cursor()
    cur.execute('set names utf8;')

    sql='''create table if not exists pgv_stat_mid.xmp_week_avg(mdate varchar(10),source varchar(10),
           1dayavg varchar(10),3dayavg varchar(10),7dayavg varchar(10),14dayavg varchar(10),28dayavg varchar(10),weekavg varchar(10))
           character set utf8;
        '''
    cur.execute(sql)
    conn.commit()
    #先清空中间表数据
    sql="delete from pgv_stat_mid.xmp_week_avg;" #这条语句有问题
    cur.execute(sql)
    conn.commit()

    ##计算过程
    calc_avg_week(conn,cur,stadate,tblname)

    ##关闭连接
    cur.close()
    conn.close()


