#!/usr/bin/env python27
#-*-coding:utf8-*-
__author__ = 'yjm'
'''
  功能注释：片库在线（竞品）播放详情和按类型汇总统计
'''

import MySQLdb
import json
import time
import urllib2
import os
import sys
import hues
from datetime import date, datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf8')

g_tool_hive="/usr/local/complat/cdh5.10.0/hive/bin/hive"
datapath=os.getcwd()
datapath=datapath.replace("/bin","/data")
if not os.path.exists(datapath):
    os.mkdir(datapath)


'''
    片库按类型播放统计
'''
class XMPTypePlay():
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="hive")
        self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.cur.execute("use pgv_stat_yingyin")
        self.cur.execute('set names utf8')
        self.id_map={}
        self.exportdata="%s/xmp_online_play_pre_%s" %(datapath,stadate)
        self.outdata="%s/xmp_online_play_%s" %(datapath,stadate)

    def __del__(self):
        self.cur.close()
        self.conn.close()

    # 根据movieid获取名称和类型
    def _getTypeTitle(self,movieid):
        url='http://media.v.xunlei.com/pc/info?movieid='+movieid
        headers ={
            "Host":"media.v.xunlei.com",
            "Referer": "http://media.v.xunlei.com",
            "cookie":"client=pc;version=5.1.0.3054"
        }
        request=urllib2.Request(url,None,headers)
        resonse=urllib2.urlopen(request)
        content=resonse.read().decode('utf8')
        pdict=json.loads(content)
        mtype=pdict.get('type','Unknown')
        mtitle=pdict.get('title','Unknown')
        self.id_map[movieid]=[mtitle,mtype]
        return mtitle,mtype

    # 数据准备(hive数据到本地文件)
    def export_data(self):
        hues.info("原始播放数据导出")
        hivecmd="%s -e \"use xmp_odl;select fu1,fu4 from xmpconv where ds='%s' and fu3='XMP-JingPin' and length(fu1)=16;\"> %s" %(g_tool_hive,stadate,self.exportdata)
        print hivecmd
        if os.system(hivecmd) != 0:
            hues.error("get jingpin play from xmpconv failed!")
            sys.exit(1)


    # 数据处理
    def data_proc(self):
        hues.info("导出数据处理，合并类型和title")
        fout=open(self.outdata,'w')
        with open(self.exportdata,'r') as f:
            try:
                for line in f:
                    peerid,movieid=line.strip('\n').split('\t')
                    if len(movieid)==0:
                        mtitle=" "
                        mtype="shortvideo"
                    else:
                        movieid="mi"+movieid
                        if movieid in self.id_map:
                            mtitle,mtype=self.id_map[movieid]
                        else:
                            mtitle,mtype=self._getTypeTitle(movieid)
                            time.sleep(0.1)
                    outres=peerid+"\t"+mtitle+"\t"+mtype+"\t"+movieid
                    print "[outres]:"+outres
                    fout.write(outres+"\n")
            except Exception,e:
                s=sys.exc_info()
                hues.error(line,str(e),s[2].tb_lineno)
        fout.close()

    # 导入数据
    def import_sql(self):
        hues.info("导入中间表")
        try:
            csql="create table if not exists pgv_stat_mid.xmp_online_play_detail(peerid varchar(20),title varchar(250),type varchar(20),movieid varchar(10))ENGINE=MyISAM DEFAULT CHARSET utf8;"
            self.cur.execute(csql)

            del_sql="delete from pgv_stat_mid.xmp_online_play_detail;"
            self.cur.execute(del_sql)

            load_sql="load data local infile '%s' into table pgv_stat_mid.xmp_online_play_detail character set utf8 fields terminated by '\t';" %(self.outdata)
            self.cur.execute(load_sql)
        except Exception,e:
            s=sys.exc_info()
            hues.error("导入中间表失败",str(e),s[2].tb_lineno)
            return

        hues.info("结果汇总")
        try:
            # 详情表
            csql="create table if not exists xmp_online_play_detail(date varchar(10),title varchar(100),type varchar(20),movieid varchar(10),pv int,uv int)ENGINE=MyISAM DEFAULT CHARSET utf8;"
            self.cur.execute(csql)

            del_sql="delete from xmp_online_play_detail where date='%s';" %(stadate)
            self.cur.execute(del_sql)

            insert_sql="insert into xmp_online_play_detail select '%s',title,type,movieid,count(*),count(distinct peerid) from pgv_stat_mid.xmp_online_play_detail group by movieid;" %(stadate)
            self.cur.execute(insert_sql)

            # 汇总表
            csql="create table if not exists xmp_online_play_total(date varchar(10),type varchar(50),pv int,uv int)ENGINE=MyISAM DEFAULT CHARSET utf8;"
            self.cur.execute(csql)

            del_sql="delete from xmp_online_play_total where date='%s';" %(stadate)
            self.cur.execute(del_sql)

            # 按类型汇总
            insert_sql="insert into xmp_online_play_total select '%s',type,count(*),count(distinct peerid) from pgv_stat_mid.xmp_online_play_detail group by type;" %(stadate)
            self.cur.execute(insert_sql)

            # 全网汇总
            insert_sql="insert into xmp_online_play_total select '%s','all',count(*),count(distinct peerid) from pgv_stat_mid.xmp_online_play_detail;" %(stadate)
            self.cur.execute(insert_sql)
        except Exception,e:
            s=sys.exc_info()
            hues.error("汇总和导入失败",str(e),s[2].tb_lineno)


# 测试入口
if __name__ == "__main__":
    if len(sys.argv)<2:
        yesterday = date.today() - timedelta(days=1)
        stadate = yesterday.strftime("%Y%m%d")
    else:
        stadate=sys.argv[1]

    xtp=XMPTypePlay()
    xtp.export_data()
    xtp.data_proc()
    xtp.import_sql()

