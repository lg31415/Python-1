#!/usr/bin/env python
#-*-coding:utf8-*-
__author__ = 'yjm'

import time
import os,sys
from datetime import date,datetime,timedelta



# 基本日期操作
def getdate():
    #获取当前日期
    today=time.strftime('%Y%m%d',time.localtime(time.time()))
    end_day=date(int(today[0:4]),int(today[4:6]),int(today[-2:]))-timedelta(days=30)

    # 七天前
    calc_day = (date.today()).strftime("%Y%m%d")
    week_day_begin = (date.today() - timedelta(days=7)).strftime("%Y%m%d")
    week_day_end = (date.today() - timedelta(days=1)).strftime("%Y%m%d")
    print week_day_end
    print week_day_begin


#区间段
def datedur():
    #利用时间日期计算函数
    startdate_struct=time.strptime('20150509','%Y%m%d') #time.struct_time
    startdate_date=date(startdate_struct.tm_year,startdate_struct.tm_mon,startdate_struct.tm_mday) #datetime.date
    startdate_string=time.strftime('%Y%m%d',startdate_date.timetuple())

    enddate_struct=time.strptime('20151020','%Y%m%d')
    enddate_date=date(enddate_struct.tm_year,enddate_struct.tm_mon,enddate_struct.tm_mday) #datetime.date
    enddate_string=time.strftime('%Y%m%d',enddate_date.timetuple())

    while startdate_string<enddate_string:
        print(startdate_string)
        startdate_date=startdate_date+timedelta(days=1)
        startdate_string=time.strftime('%Y%m%d',startdate_date.timetuple())

if __name__ == "__main__":
    if len(sys.argv)<2:
        stadate='20150817' #raw_input('Please input the stadate:')
    else:
        stadate=sys.argv[1]
    #getdate()
    datedur()
