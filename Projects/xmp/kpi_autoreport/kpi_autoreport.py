#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:kpi自动报表配置
	Ref:http://www.jb51.net/article/60510.htm
	State：注意日期处理
	Date:2017/5/3
	Author:tuling56
'''
import re, os, sys
#import hues

reload(sys)
sys.setdefaultencoding('utf-8')


import xlrd
import xlwt
import MySQLdb
from datetime import date,datetime,timedelta

if len(sys.argv)<2:
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
else:
    lastmon_first=sys.argv[1]
    lastmon_last=sys.argv[2]
    lastmon=lastmon_first[0:6]
    lastlastmon=str(int(lastmon)-1)


curdir=os.getcwd()
datapath=curdir.replace("/bin","/data")

'''
	数据的生成和报表的配置
'''
class KPIAutoReport():
    def __init__(self):
        self.infile="{datapath}/kpi_autoreport_{lastlastmon}.xls".format(datapath=datapath,lastlastmon=lastlastmon)
        self.outfile="{datapath}/kpi_autoreport_{lastmon}.xls".format(datapath=datapath,lastmon=lastmon)
        self.infile="E:\\Code\\Git\\Python\\data\\kpi_autoreport.xlsx"
        self.outfile="E:\\Code\\Git\\Python\\data\\kpi_autoreport_new.xls"
        self.newdau_data=[('2016555',20233),('2016023',77777)]
        self.newmuv_data=[('Jar-2017',66666),]

    # 数据生成
    def gen_newdata(self):
        # dau数据统计
        print lastmon_first
        print lastmon_last
        try:
            conn=MySQLdb.connect(host='localhost',user='xxx',passwd='xxxx',port=3307,db='xxxxx',unix_socket="/tmp/mysql5.sock")
            cur=conn.cursor()
            cur.execute('set names utf8')
        except Exception,e:
            print('open %s db fail,exit'%('pgv_stat'))
            sys.exit()

        newdau_sql="select date,active_user from pgv_stat.xmp_kpi_active where date>='{lastmon_first}' and date<='{lastmon_last}' order by date desc;".format(lastmon_first=lastmon_first,lastmon_last=lastmon_last)
        print newdau_sql
        cur.execute(newdau_sql)
        self.newdau_data=cur.fetchall()

        #月覆盖数据统计
        newmuv_sql="select concat(left(monthname(fdate),3),'-',right(year(fdate),2)), online_num from  pgv_stat.xmp_cover_mon where fdate='${lastmon_first}';".format(lastmon_first=lastmon_first)
        print newmuv_sql
        cur.execute(newmuv_sql)
        self.newmuv_data=cur.fetchall()

    # 报表制作
    def gen_report(self):
        workbook_read=xlrd.open_workbook(self.infile)
        workbook_write=xlwt.Workbook()

        # 格式控制(有问题)
        #styletitle = xlwt.XFStyle()
        #styletitle.alignment='right'
        #styletitle.font='bold'

        #stylecontent = xlwt.XFStyle()
        #stylecontent.alignment='horiz right'


        for sheet_name in workbook_read.sheet_names():
            print sheet_name
            table_read=workbook_read.sheet_by_name(sheet_name)
            table_write=workbook_write.add_sheet(sheet_name)
            colnames=table_read.row_values(0)      # 列名(第一行的数据)
            nrows,ncols=table_read.nrows,table_read.ncols
            # 写入列名
            for i in range(len(colnames)):
                table_write.write(0,i,colnames[i])#,styletitle)

            # 写入新数据
            if sheet_name=='用户DAU':
                for rown,rowlist in enumerate(self.newdau_data):
                    for coln,cold in enumerate(rowlist):
                        table_write.write(1+rown,coln,cold)#,stylecontent)
            elif sheet_name=='MUV':
                for rown,rowlist in enumerate(self.newmuv_data):
                    for coln,cold in enumerate(rowlist):
                        table_write.write(1+rown,coln,cold)#,stylecontent)
            else:
                print '未知工作表'
                return 1

            # 写入旧数据
            for rownum in range(1,nrows):
                rowvalues=table_read.row_values(rownum)
                for coln,cold in enumerate(rowvalues): #读出来的是日期格式，要进行转换
                    # 如果读出的是日期格式
                    if(table_read.cell_type(rownum,coln)==3):
                        date_value=xlrd.xldate_as_tuple(table_read.cell_value(rownum,coln),workbook_read.datemode)
                        cold=date(*date_value[:3]).strftime('%b-%Y')
                        print cold
                    if sheet_name=='用户DAU':
                        table_write.write(len(self.newdau_data)+rownum,coln,cold)#,stylecontent)
                    elif sheet_name=='MUV':
                        table_write.write(len(self.newmuv_data)+rownum,coln,cold)#,stylecontent)
                    else:
                        print '未知工作表'

        workbook_read.release_resources()
        workbook_write.save(self.outfile)  #注意保存格式是xls,不要是xlsx，否则提示错误打不开

    # 清除历史
    def cleartmp(self):
        os.remove(self.infile)

# 测试入口
if __name__ == "__main__":
    kpireport=KPIAutoReport()
    #kpireport.gen_newdata()
    kpireport.gen_report()
    #kpireport.cleartmp()

