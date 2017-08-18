#-*coding:utf-8-*-
__author__ = 'yjm'
'''
    功能注释：日期和时间类学习
    状态:持续更新中
'''

import time #time也是一个模块？？
import datetime  #datetime是一个模块
from datetime import date,datetime,timedelta #time
import sys
import os
import hues

# 当前时间
def datebasic():
    after_time = int(time.time())-1*24*3600
    hues.info(u"%s~~%s未有豆瓣数据更新" %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(after_time)),time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())))

#最简单的日期操作
def dataaddsub():
    if len(sys.argv) <= 1:
	yestoday = date.today() - timedelta(days=1)
	yestoday = yestoday.strftime("%Y%m%d")
    else:
        yestoday = sys.argv[1]

    '''
    start_day = date(2015,5,1)  #date类型的构造函数
    endday = date(2015,6,25)
    '''

    #daydelta = timedelta(days=1)

    start_day=date(int(yestoday[0:4]),int(yestoday[4:6]),int(yestoday[-2:]))
    endday   =date(int(yestoday[0:4]),int(yestoday[4:6]),int(yestoday[-2:]))
    print(start_day,endday)


#字符串转换成时间戳
def str2date():
    time1="2015-09-28 23:42:00"
    timeArray=time.strptime(time1,"%Y-%m-%d %H:%M:%S") #字符串转日期时间结构体time.struct_time
    timeStamp=int(time.mktime(timeArray))   #日期时间结构体转时间戳
    print(timeStamp)

    dateC=datetime(2010,6,6,8,14,59) #2010-06-06 08:14:59  datetime类型的构造函数
    timestamp=time.mktime(dateC.timetuple())  #datetime类型转日期时间结构体datetime.timetuple()
    print timestamp

#时间戳(以毫秒计算)转日期
def timeStamp2date():
    timeArray2=time.ctime(1332586088)    #其输出是'Thu Jan 01 14:30:55 1970'，一个可显示的时间日期字符串
    print(type(timeArray2),timeArray2)
    print type(time.localtime(time.time()))

    #方法二
    ltime=time.localtime(1374047395) #其中1442387754代表时间戳
    timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    print timeStr


#格式转换
def formatTrans():
    print('type(datatime.now())',type(datetime.now()),'-',datetime.now())

    #日期时间字符串格式更改
    originformat='20150912'
    t_tuple1=time.strptime(originformat,'%Y%m%d')
    newformat=time.strftime("%Y/%m/%d %H-%M-%S",t_tuple1)
    print newformat

    #日期时间转换成日期
    mdate=datetime.date(datetime.now())
    print  'Nowdate:',mdate


#日期运算
def dataOper():
    #字符串转日期
    stadate_struct=time.strptime('20150923','%Y%m%d')  #time.struct_time
    stadate_date=date(stadate_struct.tm_year,stadate_struct.tm_mon,stadate_struct.tm_mday)  #datetime.date
    print stadate_date  #2015-09-23
    #转日期后再计算
    calcdate=stadate_date-timedelta(month=12,days=1)  #datetime.date类型
    calcdate_str = '%04d%02d%02d' %(calcdate.year, calcdate.month, calcdate.day)
    #yesdate_str=time.strftime('%Y%m%d',yesdate.timetuple())        #20150922
    print calcdate_str

#日期运算２
def dateOper2():
    stadate=date.today()-timedelta(days=3)   # 日期类型
    #stadate = '%04d%02d%02d' %(stadate.year, stadate.month, stadate.day)
    if(date.today().day==3):
        print '每月2号开始计算上一个月的数据'
    else:
        print '不是2号,退出'
        sys.exit()
    #lastmon_first='{year}{month}01'.format(year=stadate.year,month=stadate.month)
    lastmon_first=date(stadate.year,stadate.month,1).strftime("%Y%m%d")
    lastmon_last=stadate.strftime("%Y%m%d")
    lastmon=stadate.strftime("%Y%m")
    lastlastmon=date(stadate.year,stadate.month-1,1).strftime("%Y%m")
    #lastlastmon=str(int(lastmon)-1)

# 求当月的天数，第一天和最后一天
def getMonthFirstDayAndLastDay(year=None, month=None):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 当月的第一天，datetime.date类型
              lastDay: 当月的最后一天，datetime.date类型
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    # 获取当月的第一天
    firstDay = datetime.date(year=year, month=month, day=1)
    lastDay = datetime.date(year=year, month=month, day=monthRange)

    return firstDay, lastDay


'''
    计算两个日期的时间之差：转化为天，转化为时间戳
'''

#从一个日期到另一个日期之间的所有日期
def allIntervalDate():
    startdate_str='20150509'
    startdate_struct=time.strptime(startdate_str,'%Y%m%d') #time.struct_time
    startdate_date=date(startdate_struct.tm_year,startdate_struct.tm_mon,startdate_struct.tm_mday) #datetime.date
    startdate_string=time.strftime('%Y%m%d',startdate_date.timetuple())

    enddate_str='20151020'
    enddate_struct=time.strptime(enddate_str,'%Y%m%d')
    enddate_date=date(enddate_struct.tm_year,enddate_struct.tm_mon,enddate_struct.tm_mday) #datetime.date
    enddate_string=time.strftime('%Y%m%d',enddate_date.timetuple())

    datelist=[]
    while startdate_string<enddate_string:
        print(startdate_string)
        startdate_date=startdate_date+timedelta(days=1)
        startdate_string=time.strftime('%Y%m%d',startdate_date.timetuple())
        datelist.append(startdate_string)

    return  datelist;


'''
    利用其它模块求日期间隔
'''
#import  dateutils
from dateutils import relativedelta
from dateutil.parser import *

def mdateutil():
    startdate_struct=time.strptime('20150923','%Y%m%d')  #time.struct_time
    start_date=date(startdate_struct.tm_year,startdate_struct.tm_mon,startdate_struct.tm_mday)  #datetime.date
    now_date=datetime.date(datetime.now())  #date
    daydiff=relativedelta(now_date,start_date) # 参数是两个日期类型，返回是差的日期数：relativedelta(months=+2, days=+22)
    print(daydiff)

def datediff():
    pass



'''
    文件日期参与的计算
'''
def cmpdate():
    #删除过期文件
    today=time.strftime('%Y%m%d',time.localtime(time.time()))
    end_day=date(int(today[0:4]),int(today[4:6]),int(today[-2:]))-timedelta(days=7)

    file="mdict.py"
    t=os.stat(file)[8]  # 获取文件的修改日期
    file_mdate=time.strftime('%Y%m%d',time.localtime(t))
    delte_before='%04d%02d%02d' %(end_day.year, end_day.month, end_day.day)  # 在此日期之前的全部删除
    if file_mdate < delte_before:
        #os.remove(file)
        print "file %s has deleted!!!" % file



'''
    绝对时间
'''
def absolutetime():
    #方案0
    lt=time.localtime()  #time.struct_time,获取当前时间的年月日时分秒等信息
    print lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec,lt.tm_wday,lt.tm_yday,lt.tm_isdst
    t = (2009, 2, 17, 17, 3, 38, 1, 48, 0)  #年月日时分秒等信息
    time.mktime(t)      #得到时间戳

    #时间戳转日期datetime.fromtimestamp(time.time())

    #方案1
    curtime=datetime.now()
    dt=datetime.datetime(2010,11,12,13,14,15,16)  #datetime.datetime
    print dt.year, dt.month, dt.day,dt.hour,dt.minute,dt.second,dt.microsecond
    dtdur=dt-timedelta(days=1,seconds=1)
    durst = (2009, 2, 17, 17, 3, 38, 1, 48, 0)
    dtdur.timetuple()    # 将datetime类型转换位time.struct_time
    time.mktime(durst)


    #测试
    curtime=datetime.now()
    diff_time=curtime-timedelta(minutes=1)
    diff_time_start=(diff_time.year,diff_time.month,diff_time.day,diff_time.hour,diff_time.minute,0,0,0,-1)
    diff_time_end=(diff_time.year,diff_time.month,diff_time.day,diff_time.hour,diff_time.minute,59,0,0,-1)
    diff_time_start_stamp=int(time.mktime(diff_time_start))
    diff_time_end_stamp=int(time.mktime(diff_time_end))
    print "diff_time_start_stamp:",diff_time_start_stamp
    print "diff_time_end_stamp:",diff_time_end_stamp

    print "curtime:",curtime
    print "diff_time_start_stamp:",datetime.fromtimestamp(diff_time_start_stamp)
    print "diff_time_end_stamp:",datetime.fromtimestamp(diff_time_end_stamp)





# 主测试函数
if __name__=='__main__':
    #str2date()
    #timeStamp2date()
    #formatTrans()
    #dataOper()
    mdateutil()
    #cmpdate()



