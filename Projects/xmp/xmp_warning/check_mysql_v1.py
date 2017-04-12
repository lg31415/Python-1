#!/usr/bin/env python
# -*- coding: utf8 -*-
import MySQLdb
import os,sys
import time
from datetime import date,  datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

file_path=os.getcwd()
file_path=file_path.replace("/bin","/data")

if len(sys.argv) <= 1:
	yesterday = date.today() - timedelta(days=1)
	yesterday = yesterday.strftime("%Y%m%d")
else:
	yesterday = sys.argv[1]


conn = MySQLdb.connect(host="localhost", user="root", passwd="hive")
#cur = conn.cursor(MySQLdb.cursors.DictCursor)
cur=conn.cursor()
cur.execute("use pgv_stat")

warnfile="%s/warning_%s" %(file_path,yesterday)

## 安装卸载
def install_warning(f):
	tablea="select date,sum(install_end) as s_install_end from xmp_install where date>=date_sub(curdate(),interval 7 day) group by date"
	tableb="select date,sum(install_end) as s_install_end from xmp_install where date>=date_sub(curdate(),interval 14 day) group by date"
	whatis="a.date as '日期',a.s_install_end as '总安装量',concat(round((a.s_install_end-b.s_install_end)*100/b.s_install_end,2),'%') as '周同比'"
	sql = "SELECT {whatis} FROM ({tablea}) a INNER JOIN ({tableb}) b on b.date=DATE_FORMAT(DATE_SUB(a.date,INTERVAL 7 day),'%Y%m%d') order by a.date desc".format(whatis=whatis,tablea=tablea,tableb=tableb)
	print "安装sql:\n",sql

	cur.execute(sql)
	results = cur.fetchall()

	downnum=0
	maxdown=0
	for date,num,tongbi in results:
		print date,num,tongbi
		if float(tongbi.replace('%',''))<0:
			downnum+=1
			maxdown=maxdown if maxdown<tongbi else tongbi
	print "[downnum]:",downnum,"[maxdown]:",maxdown
	if downnum==7 and maxdown<-5:
		installwarn="安装卸载报警：\t连续七日周同比下跌，且最大单日跌幅超过-5%\n"
		f.write(installwarn)
	
		
## 播放统计
def play_warning(f):
	tablea="select date,total_vv,total_uv from xmp_total_vod where date>=DATE_SUB(curdate(),INTERVAL 7 day) and channel='all' and version=0"
	tableb="select date,total_vv,total_uv from xmp_total_vod where date>=DATE_SUB(curdate(),INTERVAL 14 day) and channel='all' and version=0"
	whatis="a.date as '日期',a.total_vv as '总播次数',concat(round((a.total_vv-b.total_vv)*100/b.total_uv,2),'%') as '次数周同比',a.total_uv as '总播放人数',concat(round((a.total_uv-b.total_uv)*100/b.total_uv,2),'%') as '人数周同比'"
	sql = "SELECT {whatis} FROM ({tablea}) a INNER JOIN ({tableb}) b on b.date=DATE_FORMAT(DATE_SUB(a.date,INTERVAL 7 day),'%Y%m%d')".format(whatis=whatis,tablea=tablea,tableb=tableb)
	print "播放sql:\n",sql

	cur.execute(sql)
	results = cur.fetchall()
	
	downnum=0
	maxvvdown,maxuvdown=0,0
	for date,total_vv,total_vv_weekratio,total_uv,total_uv_weekratio in results: 
		print date,total_vv,total_vv_weekratio,total_uv,total_uv_weekratio
		if float(total_vv_weekratio.replace('%',''))<0 or float(total_uv_weekratio.replace('%',''))<0:
			downnum+=1
			maxvvdown=total_vv_weekratio if maxvvdown>total_vv_weekratio else maxvvdown
			maxuvdown=total_uv_weekratio if maxuvdown>total_uv_weekratio else maxuvdown
	print "[downnum]:",downnum,"[maxvvdown]:",maxvvdown,"[maxuvdown]:",maxuvdown
	if downnum==7 and (maxvvdown<-5 or maxuvdown<-5):
		playwarn="播放统计报警：\t连续七日周同比下跌，且最大单日跌幅超过-5%\n"
		f.write(playwarn)



## KPI
def kpi_warning(f):
	tablea="xmp_kpi_active"
	tableb="xmp_kpi_active"
	sql = "SELECT a.date as '日期',a.active_user as 'DAU',concat(round((a.active_user-b.active_user)*100/b.active_user,2),'%') as 'DAU周同比' FROM {tablea} a INNER JOIN {tableb} b on b.date=DATE_FORMAT(DATE_SUB(a.date,INTERVAL 7 day),'%Y%m%d') WHERE a.date>=DATE_SUB(CURDATE(),INTERVAL 7 day) order by a.date desc;".format(tablea=tablea,tableb=tableb)
	print "kpi sql:\n",sql

	cur.execute(sql)
	results = cur.fetchall()

	downnum=0
	maxdown=0
	for date,dau,tongbi in results: 
		print date,dau,tongbi
		if float(tongbi.replace('%',''))<0:
			downnum+=1
			maxdown=maxdown if maxdown<tongbi else tongbi
	print "[downnum]:",downnum,"[maxdown]:",maxdown
	if downnum==7 and maxdown<-5:
		kpiwarn="KPI报警:\t连续七日周同比下跌，且最大单日跌幅超过-5%\n"
		f.write(kpiwarn)


if __name__=="__main__":
	f=open(warnfile,'w+')
	install_warning(f)
	#play_warning(f)
	#kpi_warning(f)
	f.close()




