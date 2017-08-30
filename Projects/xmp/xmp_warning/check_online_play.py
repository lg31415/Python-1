#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
    功能：在线播放报警
    Author:yuanjunmiao@xunlei.com
    日期：2017年8月30日
'''

import os,sys
import time
import MySQLdb
from datetime import date, datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) <= 1:
    yesterday = date.today() - timedelta(days=1)
    yesterday = yesterday.strftime("%Y%m%d")
else:
    yesterday = sys.argv[1]

file_path=os.getcwd()
file_path=file_path.replace("/bin","/data")

warnfile="%s/warning_%s.txt" %(file_path,yesterday)
warnfile_detail="%s/warning_detail_%s.txt" %(file_path,yesterday)


class OnlinePlayWarn():
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="hive")
        self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.cur.execute("use pgv_stat")

        # 数据生成
        self.ferror=open(warnfile,'w+')
        self.fdetail=file(warnfile_detail,'w+')

        # 定义单日跌幅上限和连续跌幅上限
        self.cur_limit=-15
        self.sum_limit=-25

    def __del__(self):
        self.cur.close()
        self.conn.close()
        self.ferror.close()
        self.fdetail.close()


    ## 播放统计报警
    def play_warning_total(self):
        tablea="select date,jingpin_pv,jingpin_uv from xmp_jingpin where date>=date_sub(curdate(),interval 7 day)"
        tableb="select date,jingpin_pv,jingpin_uv from xmp_jingpin where date>=date_sub(curdate(),interval 14 day)"
        whatis="a.date as '日期',b.date as '上周同期'," \
               "a.jingpin_pv as '总播次数',b.jingpin_pv as '上周同期播放次数',concat(round((a.jingpin_pv-b.jingpin_pv)*100/b.jingpin_pv,2),'%') as '次数周同比'," \
               "a.jingpin_uv as '总播放人数',b.jingpin_uv as '上周同期播放人数',concat(round((a.jingpin_uv-b.jingpin_uv)*100/b.jingpin_uv,2),'%') as '人数周同比'"
        sql = "SELECT {whatis} FROM ({tablea}) a INNER JOIN ({tableb}) b on b.date=DATE_FORMAT(DATE_SUB(a.date,INTERVAL 7 day),'%Y%m%d') order by a.date desc".format(whatis=whatis,tablea=tablea,tableb=tableb)
        print "\033[1;31m在线播放sql:\033[0m" #,sql
        self.cur.execute(sql)
        results = self.cur.fetchall()

        downnum=0
        maxvvdown,maxuvdown=0,0
        sumvvdown,sumuvdown=0,0
        play_info="\n日期(上周同期)\t总播放次数\t上周同期播放次数\t总播放次数周同比\t总播放人数\t上周同期总播放人数\t总播放人数周同比\n"
        iscur=0
        for date,lwdate,total_vv,lwtotal_vv,total_vv_weekratio,total_uv,lwtotal_uv,total_uv_weekratio in results:

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

        playwarn="播放统计报警:\t"
        if downnum==7:
            playwarn+="连续七日周同比下跌 "

        if cur_total_uv_weekratio<self.cur_limit or cur_total_vv_weekratio<self.cur_limit:
            playwarn+="昨日跌幅超过"+str(abs(self.cur_limit))+'%'

        if sumvvdown<self.sum_limit or sumuvdown<self.sum_limit:
            playwarn+="近七日跌幅和超过"+str(abs(self.sum_limit))+'%'

        if playwarn!="播放统计报警:\t":
            playwarn+="\n\n"
            play_info+=playwarn
            self.f.write(playwarn)
        self.fdetail.write(play_info)

    ## 在线播放按站点报警
    def play_warning_bysite(self):
        sites=['iqiyi','letv','youku','hunantv','qq','sohu']
        sites=map(lambda site:site+'_pv',sites)
        sites=','.join(sites)

        tablea="select date,%s from xmp_jingpin where date>=date_sub(curdate(),interval 7 day)" %(sites)
        tableb="select date,%s from xmp_jingpin where date>=date_sub(curdate(),interval 14 day)" %(sites)

        header=','.join()
        whatis="a.date as '日期',b.date as '上周同期',a.iqiyi_pv as '上',a.channel as '渠道',a.s_install_end as '总安装量',b.s_install_end as '上周同期总安装量',concat(round((a.s_install_end-b.s_install_end)*100/b.s_install_end,2),'%') as '总装周同比',a.s_install_new as '全新安装量',b.s_install_new as '上周同期全新安装量',concat(round((a.s_install_new-b.s_install_new)*100/b.s_install_new,2),'%') as '全新周同比'"
        sql = "select {whatis} from ({tablea}) a inner join ({tableb}) b on b.date=date_format(date_sub(a.date,interval 7 day),'%y%m%d') order by a.date desc".format(whatis=whatis,tablea=tablea,tableb=tableb)


        self.cur.execute(sql)
        results = self.cur.fetchall()

        downnum=0
        maxtotaldown,maxnewdown=0,0
        sumtotaldown,sumnewdown=0,0
        install_info="\n日期(上周同期)\t渠道\t总装\t上周同期总装\t总装周同比\t全新安装\t上周同期全新安装\t全新安装周同比\n"
        iscur=0
        for date,lwdate,channel,total,lwtotal,total_tongbi,new,lwnew,new_tongbi in results:
            #print date,total,total_tongbi,new,new_tongbi
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

        installwarn=channel+"渠道:\t"
        if downnum==7:
            installwarn+="连续七日周同比下跌 "

        if cur_total_tongbi<self.cur_limit or cur_new_tongbi<self.cur_limit:
            installwarn+="昨日跌幅超过"+str(abs(self.cur_limit))+'%'

        if sumtotaldown<self.sum_limit or sumnewdown<self.sum_limit:
            installwarn+="近七日跌幅和超过"+str(abs(self.sum_limit))+'%'

        if installwarn!=channel+"渠道:\t":
            installwarn+="\n\n"
            install_info+=installwarn
            self.ferror.write(installwarn)
        self.fdetail.write(install_info)

#程序入口
if __name__=="__main__":
    opw=OnlinePlayWarn()
    opw.play_warning_total()
    opw.play_warning_site()


