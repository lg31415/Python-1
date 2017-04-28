#!/usr/bin/env python
#coding: utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#add by yuanjunmiao@xunlei.com 2017-03-07 Thu
import time
from datetime import date,datetime,timedelta

class XMPDateStamp():
	def __init__(self,days= 0, hours=0,minutes=0):
		if not isinstance(days,int) or not isinstance(days,int) or not isinstance(minutes,int):
			print "[wrong paras]:paras type must be int"
			sys.exit()
		
		self.days=days
		self.hours=hours
		self.minutes=minutes

	def GetDiffStampDur(self):
		if self.days==0 and self.hours==0 and self.minutes==0:
			return int(time.mktime(time.localtime()))
		
		curtime=datetime.now()
		diff_time=curtime-timedelta(days=self.days,hours=self.hours,minutes=self.minutes)
		if self.days!=0:
			hour_start=0
			hour_end=23
			minute_start=0
			minute_end=59
			second_start=0
			second_end=59
		if self.hours!=0:
			hour_start=diff_time.hour
			hour_end=diff_time.hour
			minute_start=0
			minute_end=59
			second_start=0
			second_end=59
			
		if self.minutes!=0:
			hour_start=diff_time.hour
			hour_end=diff_time.hour
			minute_start=diff_time.minute
			minute_end=diff_time.minute
			second_start=0
			second_end=59

		
		diff_time_start=(diff_time.year,diff_time.month,diff_time.day,hour_start,minute_start,second_start,0,0,-1)
		diff_time_end=(diff_time.year,diff_time.month,diff_time.day,hour_end,minute_end,second_end,0,0,-1)

		diff_time_start_stamp=int(time.mktime(diff_time_start))
		diff_time_end_stamp=int(time.mktime(diff_time_end))

		return diff_time_start_stamp,diff_time_end_stamp


 
if __name__ == '__main__':
	diff_stamp=XMPDateStamp(hours=1,minutes=-1,days=1)
	diff_time=diff_stamp.GetDiffStampDur()
	if isinstance(diff_time,int):
		print "curtime_stamp:",diff_time
		print "curtime_datetime:",datetime.fromtimestamp(diff_time)
	else:
		diff_time_start_stamp,diff_time_end_stamp=diff_time
		print "diff_time_start_stamp:",diff_time_start_stamp
		print "diff_time_end_stamp:",diff_time_end_stamp
		print "diff_time_start_datetime:",datetime.fromtimestamp(diff_time_start_stamp)
		print "diff_time_end_datetime:",datetime.fromtimestamp(diff_time_end_stamp)
	
	print '---------------------------------------------------'

