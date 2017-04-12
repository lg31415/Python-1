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

    #1日留存的最晚（更早之前以有）
    date1=stadate_date+timedelta(days=1)
    date1_str = '%04d%02d%02d' %(date1.year, date1.month, date1.day)
    print '[date1_str]\n',date1_str

    #3日留存的最晚（更早之前已有）
    date3=stadate_date+timedelta(days=3)
    date3_str = '%04d%02d%02d' %(date3.year, date3.month, date1.day)
    print '[date3_str]\n',date3_str

    #7日留存的最晚（更早之前已有）
    date7=stadate_date+timedelta(days=7)
    date7_str = '%04d%02d%02d' %(date7.year, date7.month, date7.day)
    print '[date7_str]\n',date7_str

    #14日留存的最晚（更早之前已有）
    date14=stadate_date+timedelta(days=14)
    date14_str = '%04d%02d%02d' %(date14.year, date14.month, date14.day)
    print '[date14_str]\n',date14_str

    #28日留存的最晚（更早之前已有）
    date28=stadate_date+timedelta(days=28)
    date28_str = '%04d%02d%02d' %(date28.year, date28.month, date28.day)
    print '[date28_str]\n',date28_str

    #1日留存的开始和结束日期
    if(date1_str<=yesdate_str):
        startdate1=stadate_date-timedelta(days=7)
        enddate1=stadate_date                          #datetime.date
    else:
        diffday=(date1-yesdate).days
        enddate1=stadate_date-timedelta(days=diffday)
        startdate1=enddate1-timedelta(days=7)
    startdate1=time.strftime('%Y%m%d',startdate1.timetuple())
    enddate1=time.strftime('%Y%m%d',enddate1.timetuple())
    print '[startdate1-enddate1]:',startdate1,enddate1

    #3日留存的开始和结束日期
    if(date3_str<yesdate_str):
        startdate3=stadate_date-timedelta(days=7)                           #datetime.date
        enddate3=stadate_date
    else:
        diffday=(date3-yesdate).days
        enddate3=stadate_date-timedelta(days=diffday)
        startdate3=enddate3-timedelta(days=7)
    startdate3=time.strftime('%Y%m%d',startdate3.timetuple())
    enddate3=time.strftime('%Y%m%d',enddate3.timetuple())
    print '[startdate3-enddate3]:',startdate3,enddate3

    #7日留存的开始和结束日期
    if(date7_str<yesdate_str):
        startdate7=stadate_date-timedelta(days=7)                           #datetime.date
        enddate7=stadate_date
    else:
        diffday=(date7-yesdate).days
        enddate7=stadate_date-timedelta(days=diffday)
        startdate7=enddate7-timedelta(days=7)
    startdate7=time.strftime('%Y%m%d',startdate7.timetuple())
    enddate7=time.strftime('%Y%m%d',enddate7.timetuple())
    print '[startdate7-enddate7]:',startdate7,enddate7

    #14留存的开始和结束日期
    if(date14_str<yesdate_str):
        startdate14=stadate_date-timedelta(days=7)                           #datetime.date
        enddate14=stadate_date
    else:
        diffday=(date14-yesdate).days
        enddate14=stadate_date-timedelta(days=diffday)
        startdate14=enddate14-timedelta(days=7)
    startdate14=time.strftime('%Y%m%d',startdate14.timetuple())
    enddate14=time.strftime('%Y%m%d',enddate14.timetuple())
    print '[startdate14-enddate14]:',startdate14,enddate14

    #28日留存的开始和结束日期
    if(date28_str<yesdate_str):
        startdate28=stadate_date-timedelta(days=7)                           #datetime.date
        enddate28=stadate_date
    else:
        diffday=(date28-yesdate).days
        enddate28=stadate_date-timedelta(days=diffday)
        startdate28=enddate28-timedelta(days=7)
    startdate28=time.strftime('%Y%m%d',startdate28.timetuple())
    enddate28=time.strftime('%Y%m%d',enddate28.timetuple())
    print '[startdate28-enddate28]:',startdate28,enddate28


    sql="use pgv_stat;select %s as 统计日期,a.source as 安装渠道,concat(avg(if(length(a.data1)!=0,convert(a.data1,decimal(6,4)),NULL)),'%%') as 1日留存均值 from %s as a inner join xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate1,enddate1)
    print '[1sql]\n',sql
    cur.execute(sql)
    results=cur.feachall()
    for item in results:
        sql="insert into pgv_stat_mid.xmp_week_avg(mdate,source,1dayavg) values('%s','%s','%s');" %(item[0],item[1],item[2])
        cur.excute(sql)
        conn.commit()

    sql="use pgv_stat;select %s as 统计日期,a.source as 安装渠道, concat(avg(if(length(a.data3)!=0,convert(a.data3,decimal(6,4)),NULL)),'%%') as 3日留存均值 from %s as a inner join xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate3,enddate3)
    print '[3sql]\n',sql
    cur.execute(sql)
    results=cur.feachall()
    for item in results:
        sql="update pgv_stat_mid.xmp_week_avg set '3dayavg'='%s'where 'source'='%s';" %(item[2],item[1])
        cur.excute(sql)
        conn.commit()

    sql="use pgv_stat;select %s as 统计日期,a.source as 安装渠道,concat(avg(if(length(a.data7)!=0,convert(a.data7,decimal(6,4)),NULL)),'%%') as 7日留存均值 from %s as a inner join xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate7,enddate7)
    print '[7sql]\n',sql
    cur.execute(sql)
    results=cur.feachall()
    for item in results:
        sql="update pgv_stat_mid.xmp_week_avg set '7dayavg'='%s'where 'source'='%s';" %(item[2],item[1])
        cur.excute(sql)
        conn.commit()

    sql="use pgv_stat;select %s as 统计日期,a.source as 安装渠道,concat(avg(if(length(a.data14)!=0,convert(a.data14,decimal(6,4)),NULL)),'%%') as 14日留存均值 from %s as a inner join xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate14,enddate14)
    print '[14sql]\n',sql
    cur.execute(sql)
    results=cur.feachall()
    for item in results:
        sql="update pgv_stat_mid.xmp_week_avg set '14dayavg'='%s'where 'source'='%s';" %(item[2],item[1])
        cur.excute(sql)
        conn.commit()


    sql="use pgv_stat;select %s as 统计日期,a.source as 安装渠道,concat(avg(if(length(a.data28)!=0,convert(a.data28,decimal(6,4)),NULL)),'%%') as 28日留存均值 from %s as a inner join xmp_install_source_total b  on b.source=a.source where a.date=b.date and a.date>'%s' and a.date<='%s' group by a.source order by a.source;" %(stadate,tblname,startdate28,enddate28)
    print '[28sql]\n',sql
    cur.execute(sql)
    results=cur.feachall()
    for item in results:
        sql="update pgv_stat_mid.xmp_week_avg set '28dayavg'='%s'where 'source'='%s';" %(item[2],item[1])
        cur.excute(sql)
        conn.commit()



    #将查询结果输出到文件中
    sql='''set names utf8;use pgv_stat;select mdate as 日期，source as 安装渠道，1dayavg as 1日留存均值，3dayavg as 3日留存均值，7dayavg as 7日留存均值 14dayavg as 14日留存均值，28dayavg as 28日留存均值，7dayavg as 周留存均值 from xmp_week_avg;'''
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

    sql='''use pgv_stat_mid;create table if not exists xmp_avg_week(sdate varchar(10),source varchar(10),
           1dayavg varchar(10),3dayavg varchar(10),7dayavg varchar(10),14dayavg varchar(10),28dayavg varchar(10),weekavg varchar(10))
           character set utf8;
        '''
    cur.execute(sql)
    #先清空中间表数据
    #sql="use pgv_stat_mid;delete from xmp_week_avg;" #这条语句有问题
    #cur.execute(sql)
    #conn.commit()

    ##计算过程
    calc_avg_week(conn,cur,stadate,tblname)

    ##关闭连接
    cur.close()
    conn.close()


