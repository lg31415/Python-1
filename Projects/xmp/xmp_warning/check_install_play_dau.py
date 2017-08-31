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
#cur = conn.cursor(MySQLdb.cursors.DictCursor)  #使用字典的方式读取，每一行的结果都是一个字典
cur=conn.cursor()
cur.execute("use pgv_stat")

warnfile="%s/warning_%s.txt" %(file_path,yesterday)
warnfile_detail="%s/warning_detail_%s.txt" %(file_path,yesterday)
fdetail=file(warnfile_detail,'w+')

## 安装卸载
def install_warning(f,fdetail):
	# 总统计
	tablea="select date,sum(install_end) as s_install_end,sum(install_new+install_silence) as s_install_new from xmp_install where date>=date_sub(curdate(),interval 7 day) group by date"
	tableb="select date,sum(install_end) as s_install_end,sum(install_new+install_silence) as s_install_new from xmp_install where date>=date_sub(curdate(),interval 14 day) group by date"
	whatis="a.date as '当前日期',b.date as '上周同期',a.s_install_end as '总安装量',b.s_install_end as '上周同期总安装量',concat(round((a.s_install_end-b.s_install_end)*100/b.s_install_end,2),'%') as '总装周同比',a.s_install_new as '全新安装量',b.s_install_new as '上周同期全新安装量',concat(round((a.s_install_new-b.s_install_new)*100/b.s_install_new,2),'%') as '全新周同比'"
	sql = "SELECT {whatis} FROM ({tablea}) a INNER JOIN ({tableb}) b on b.date=DATE_FORMAT(DATE_SUB(a.date,INTERVAL 7 day),'%Y%m%d') order by a.date desc".format(whatis=whatis,tablea=tablea,tableb=tableb)
	print "\033[1;31m安装sql:\033[0m\n",sql

	cur.execute(sql)
	results = cur.fetchall()

	downnum=0
	maxtotaldown,maxnewdown=0,0
	sumtotaldown,sumnewdown=0,0
	install_info="日期(上周同期)\t总装\t上周同期总装\t总装周同比\t全新安装\t上周同期全新安装\t全新安装周同比\n"
	iscur=0
	for date,lwdate,total,lwtotal,total_tongbi,new,lwnew,new_tongbi in results:
		print date,total,total_tongbi,new,new_tongbi
		install_info+=date+"("+lwdate+")\t"+str(total)+"\t"+str(lwtotal)+"\t"+total_tongbi+"\t"+str(new)+"\t"+str(lwnew)+"\t"+new_tongbi+"\n"
		total_tongbi=float(total_tongbi.replace('%',''))
		new_tongbi=float(new_tongbi.replace('%',''))
		if iscur==0:
			cur_total_tongbi=total_tongbi
			cur_new_tongbi=new_tongbi
			iscur=1
		sumtotaldown+=total_tongbi
		sumnewdown+=new_tongbi
		if total_tongbi<0 and new_tongbi<0:
			downnum+=1
		maxtotaldown=maxtotaldown if maxtotaldown<total_tongbi else total_tongbi
		maxnewdown=maxnewdown if maxnewdown<new_tongbi else new_tongbi
	print "[downnum]:",downnum,"[maxtotaldown]:",maxtotaldown,"[maxnewdown]:",maxnewdown
	install_info+="[downnum]:"+str(downnum)+"\t[maxtotaldown]:"+str(maxtotaldown)+"%\t[maxnewdown]:"+str(maxnewdown)+"%\t[sumtotaldown]:"+str(sumtotaldown)+"%\t[sumnewdown]:"+str(sumnewdown)+"%\n"
	installwarn="安装卸载报警（总）:"
	if downnum==7:
		installwarn+="\t连续七日周同比下跌 "
	if cur_total_tongbi<-4 or cur_new_tongbi<-4:
		installwarn+="昨日跌幅超过-4% "
	if sumtotaldown<-5 or sumnewdown<-5:
		installwarn+="近七日跌幅和超过-5% "
	if installwarn!="安装卸载报警（总）:":
		installwarn+="\n\n"
		install_info+=installwarn
		f.write(installwarn)
	fdetail.write(install_info)

	# 重点渠道
	for channel in ['xl9','xl8','xl79','kkweb']:
		tablea="select date,'%s' as channel,sum(install_end) as s_install_end,sum(install_new+install_silence) as s_install_new from xmp_install where date>=date_sub(curdate(),interval 7 day)  and channel like '%s' group by date" %(channel,channel)
		tableb="select date,'%s' as channel,sum(install_end) as s_install_end,sum(install_new+install_silence) as s_install_new from xmp_install where date>=date_sub(curdate(),interval 14 day) and channel like '%s' group by date" %(channel,channel)
		whatis="a.date as '当前日期',b.date as '上周同期',a.channel as '渠道',a.s_install_end as '总安装量',b.s_install_end as '上周同期总安装量',concat(round((a.s_install_end-b.s_install_end)*100/b.s_install_end,2),'%') as '总装周同比',a.s_install_new as '全新安装量',b.s_install_new as '上周同期全新安装量',concat(round((a.s_install_new-b.s_install_new)*100/b.s_install_new,2),'%') as '全新周同比'"
		sql = "SELECT {whatis} FROM ({tablea}) a INNER JOIN ({tableb}) b on b.date=DATE_FORMAT(DATE_SUB(a.date,INTERVAL 7 day),'%Y%m%d') order by a.date desc".format(whatis=whatis,tablea=tablea,tableb=tableb)
		print "\033[1;31m%s安装sql:\033[0m\n%s" %(channel,sql)

		cur.execute(sql)
		results = cur.fetchall()

		downnum=0
		maxtotaldown,maxnewdown=0,0
		sumtotaldown,sumnewdown=0,0
		install_info="\n日期(上周同期)\t渠道\t总装\t上周同期总装\t总装周同比\t全新安装\t上周同期全新安装\t全新安装周同比\n"
		iscur=0
		for date,lwdate,channel,total,lwtotal,total_tongbi,new,lwnew,new_tongbi in results:
			print date,total,total_tongbi,new,new_tongbi
			install_info+=date+"("+lwdate+")\t"+channel+"\t"+str(total)+"\t"+str(lwtotal)+"\t"+total_tongbi+"\t"+str(new)+"\t"+str(lwnew)+"\t"+new_tongbi+"\n"
			total_tongbi=float(total_tongbi.replace('%',''))
			new_tongbi=float(new_tongbi.replace('%',''))
			if iscur==0:
				cur_total_tongbi=total_tongbi
				cur_new_tongbi=new_tongbi
				iscur=1
			sumtotaldown+=total_tongbi
			sumnewdown+=new_tongbi
			if total_tongbi<0 and new_tongbi<0:
				downnum+=1
			maxtotaldown=maxtotaldown if maxtotaldown<total_tongbi else total_tongbi
			maxnewdown=maxnewdown if maxnewdown<new_tongbi else new_tongbi
		print "[downnum]:",downnum,"[maxtotaldown]:",maxtotaldown,"[maxnewdown]:",maxnewdown
		install_info+="[downnum]:"+str(downnum)+"\t[maxtotaldown]:"+str(maxtotaldown)+"%\t[maxnewdown]:"+str(maxnewdown)+"%\t[sumtotaldown]:"+str(sumtotaldown)+"%\t[sumnewdown]:"+str(sumnewdown)+"%\n"
		
		installwarn=channel+"渠道:"
		if downnum==7:
			installwarn+="\t连续七日周同比下跌 "
		if cur_total_tongbi<-4 or cur_new_tongbi<-4:
			installwarn+="昨日跌幅超过-4% "
		if sumtotaldown<-5 or sumnewdown<-5:
			installwarn+="近七日跌幅和超过-5 " 
		if installwarn!=channel+"渠道:":
			installwarn+="\n\n"
			install_info+=installwarn
			f.write(installwarn)
		fdetail.write(install_info)


		
## 播放统计
def play_warning(f,fdetail):
	tablea="select date,total_vv,total_uv from xmp_total_vod where date>=DATE_SUB(curdate(),INTERVAL 7 day) and channel='all' and version=0"
	tableb="select date,total_vv,total_uv from xmp_total_vod where date>=DATE_SUB(curdate(),INTERVAL 14 day) and channel='all' and version=0"
	whatis="a.date as '日期',b.date as '上周同期',a.total_vv as '总播次数',b.total_vv as '上周同期播放次数',concat(round((a.total_vv-b.total_vv)*100/b.total_vv,2),'%') as '次数周同比',a.total_uv as '总播放人数',b.total_uv as '上周同期播放人数',concat(round((a.total_uv-b.total_uv)*100/b.total_uv,2),'%') as '人数周同比'"
	sql = "SELECT {whatis} FROM ({tablea}) a INNER JOIN ({tableb}) b on b.date=DATE_FORMAT(DATE_SUB(a.date,INTERVAL 7 day),'%Y%m%d') order by a.date desc".format(whatis=whatis,tablea=tablea,tableb=tableb)
	print "\033[1;31m播放sql:\033[0m\n",sql

	cur.execute(sql)
	results = cur.fetchall()
	
	downnum=0
	maxvvdown,maxuvdown=0,0
	sumvvdown,sumuvdown=0,0
	play_info="\n日期(上周同期)\t总播放次数\t上周同期播放次数\t总播放次数周同比\t总播放人数\t上周同期总播放人数\t总播放人数周同比\n"
	iscur=0
	for date,lwdate,total_vv,lwtotal_vv,total_vv_weekratio,total_uv,lwtotal_uv,total_uv_weekratio in results: 
		print date,total_vv,total_vv_weekratio,total_uv,total_uv_weekratio
		play_info+=date+"("+lwdate+")\t"+str(total_vv)+"\t"+str(lwtotal_vv)+"\t"+total_vv_weekratio+"\t"+str(total_uv)+"\t"+str(lwtotal_uv)+"\t"+total_uv_weekratio+"\n"
		total_vv_weekratio=float(total_vv_weekratio.replace('%',''))
		total_uv_weekratio=float(total_uv_weekratio.replace('%',''))
		if iscur==0:
			cur_total_vv_weekratio=total_vv_weekratio
			cur_total_uv_weekratio=total_uv_weekratio
			iscur=1
		sumvvdown+=total_vv_weekratio
		sumuvdown+=total_uv_weekratio
		if total_vv_weekratio<0 or total_uv_weekratio<0:
			downnum+=1
		maxvvdown=total_vv_weekratio if maxvvdown>total_vv_weekratio else maxvvdown
		maxuvdown=total_uv_weekratio if maxuvdown>total_uv_weekratio else maxuvdown
	print "[downnum]:",downnum,"[maxvvdown]:",maxvvdown,"[maxuvdown]:",maxuvdown
	play_info+="[downnum]:"+str(downnum)+"\t[maxvvdown]:"+str(maxvvdown)+"%\t[maxuvdown]:"+str(maxuvdown)+"%\t[sumvvdown]:"+str(sumvvdown)+"%\t[sumuvdown]:"+str(sumuvdown)+"%\n"
	playwarn="播放统计报警:"
	if downnum==7:
		playwarn+="\t连续七日周同比下跌 "
	if cur_total_uv_weekratio<-4 or cur_total_vv_weekratio<-4:
		playwarn+="昨日跌幅超过-4% "
	if sumvvdown<-5 or sumuvdown<-5:
		playwarn+="近七日跌幅和超过-5% "
	if playwarn!="播放统计报警:":
		playwarn+="\n\n"
		play_info+=playwarn
		f.write(playwarn)
	fdetail.write(play_info)


## KPI
def kpi_warning(f,fdetail):
	tablea="xmp_kpi_active"
	tableb="xmp_kpi_active"
	sql = "SELECT a.date as '日期',b.date as '上周同期',a.active_user as 'DAU',b.active_user as '上周同期DAU',concat(round((a.active_user-b.active_user)*100/b.active_user,2),'%') as 'DAU周同比' FROM {tablea} a INNER JOIN {tableb} b on b.date=DATE_FORMAT(DATE_SUB(a.date,INTERVAL 7 day),'%Y%m%d') WHERE a.date>=DATE_SUB(CURDATE(),INTERVAL 7 day) order by a.date desc;".format(tablea=tablea,tableb=tableb)
	print "\033[1;31mkpi sql:\033[0m\n",sql

	cur.execute(sql)
	results = cur.fetchall()

	downnum=0
	sumdown,maxdown=0,0
	kpi_info="\n日期(上周同期)\tDAU\t上周同期DAU\tDAU周同比\n"
	iscur=0
	for date,lwdate,dau,lwdau,tongbi in results: 
		print date,dau,tongbi
		kpi_info+=date+"("+lwdate+")\t"+str(dau)+"\t"+str(lwdau)+"\t"+tongbi+"\n"
		tongbi=float(tongbi.replace('%',''))
		if iscur==0:
			cur_tongbi=tongbi
			iscur=1
		sumdown+=tongbi
		if tongbi<0:
			downnum+=1
		maxdown=maxdown if maxdown<tongbi else tongbi
	print "[downnum]:",downnum,"[maxdown]:",maxdown
	kpi_info+="[downnum]:"+str(downnum)+"\t[maxdown]:"+str(maxdown)+"%\n"
	kpiwarn="KPI报警:"
	if downnum==7 or cur_tongbi<-4 or sumdown<-5:
		kpiwarn+="\t连续七日周同比下跌 "
	if cur_tongbi<-4:
		kpiwarn+="昨日跌幅超过-4% "
	if sumdown<-5:
		kpiwarn+="近七日跌幅和超过-5% "
	if kpiwarn!="KPI报警:":
		kpiwarn+="\n\n"
		kpi_info+=kpiwarn
		f.write(kpiwarn)

	fdetail.write(kpi_info)


if __name__=="__main__":
	f=open(warnfile,'w+')
	fdetail=file(warnfile_detail,'w+')
	
	install_warning(f,fdetail)
	play_warning(f,fdetail)
	kpi_warning(f,fdetail)
	
	f.close()
	fdetail.close()


