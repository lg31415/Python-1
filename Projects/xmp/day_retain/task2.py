# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：日留存计算，分按渠道和按版本
'''

import pymysql
import os

src_peerid_table="src_peerid_table"  #28天的安装数据（peerid,date,source,version）
src_online_table="src_online_table"  #某一天的在线数据（peerid）
temp_merge_table="temp_merge_table"  #中间表（数据合并使用）
result_source_remain_table="result_source_remain_table"      #结果表1:按渠道的日留存表
result_version_remain_table="result_version_remain_table"    #结果表2:按版本的日留存表

'''
  Part1: ************数据准备**************
'''

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='task3') #新建的数据库
if conn==0:
    print('open %s db fail'%('task2'))
    exit()
cur=conn.cursor()
#创建表
#ct_sql='''
#     create table if not exists src_peerid_table(peerid varchar(20),sta_date varchar(10),sta_source varchar(20),sta_version varchar(20)) character set utf8;
#     create table if not exists src_online_table(peerid varchar(20)) character set utf8;
#     create table if not exists temp_merge_table(peerid varchar(20),sta_date varchar(10),sta_source varchar(20),sta_version varchar(20)) character set utf8;
#     create table if not exists result_source_remain_table(sta_date varchar(10),sta_source varchar(20),clc_num int(7),clc_totalnum int(7),clc_remain float(5)) character set utf8;
#     create table if not exists result_version_remain_table(sta_date varchar(10),sta_version varchar(20),clc_num int(7),clc_totalnum int(7),clc_remain float(5)) character set utf8;
#      '''

ct_sql='create table if not exists src_peerid_table(peerid varchar(20),sta_date varchar(10),sta_source varchar(20),sta_version varchar(20)) character set utf8'
cur.execute(ct_sql)
conn.commit()

ct_sql='create table if not exists src_online_table(peerid varchar(20)) character set utf8'
cur.execute(ct_sql)
conn.commit()

ct_sql='create table if not exists temp_merge_table(peerid varchar(20),sta_date varchar(10),sta_source varchar(20),sta_version varchar(20)) character set utf8'
cur.execute(ct_sql)
conn.commit()

ct_sql='create table if not exists result_source_remain_table(sta_date varchar(10),sta_source varchar(20),clc_num int(7),clc_totalnum int(7),clc_remain float(5)) character set utf8'
cur.execute(ct_sql)
conn.commit()

ct_sql='create table if not exists result_version_remain_table(sta_date varchar(10),sta_version varchar(20),clc_num int(7),clc_totalnum int(7),clc_remain float(5)) character set utf8'
cur.execute(ct_sql)
conn.commit()

#数据载入
# method 1-存在的问题：The used command is not allowed with this MySQL version
'''
load_sql="load data local infile '%s' into table %s" %('xmp_28days_peerid.20150712_20150810','src_peerid_table') #28天安装数据载入
cur.execute(load_sql)
conn.commit()

load_sql="load data local infile '%s' into table %s" %('xmp_online_peerid.20150811','src_online_table') #某一天（0811）客户在线数据载入
print load_sql
cur.execute(load_sql)
conn.commit()
'''

#method2
load_cmd='''mysql -uroot -proot task2 --local-infile=1 \
       -e "load data local infile 'E://SQL//task2//xmp_28days_peerid.20150712_20150810' \
        into table src_peerid_table(peerid,sta_date,sta_source,sta_version)"
    '''
os.system(load_cmd)

load_cmd='''mysql -uroot -proot task2 --local-infile=1 \
       -e "load data local infile 'E://SQL//task2//xmp_online_peerid.20150811' \
        into table src_online_table(peerid)"
    '''
os.system(load_cmd)


'''
   Part2: **********指标计算************
'''

# 合并表生成（将一个表插入到另一个表)[此处是将在线表插入到peerid表]
merge_sql='insert into %s select * from %s' %(temp_merge_table,src_peerid_table)
cur.execute(merge_sql)
conn.commit()

merge_sql='insert into %s(peerid) select * from %s' %(temp_merge_table,src_online_table)
cur.execute(merge_sql)
conn.commit()

#temp_merge_table 复制到mid_table表,mid_table这个表的价值意义很大
merge_sql='create table if not exists mid_table ' \
          'select * from (select *,count(*) as num from temp_merge_table group by peerid) as subsel1' \
          'where date is not null order by date'
cur.execute(merge_sql)
conn.commit()

'''
mid_table的数据格式,其中num=2代表留存，1代表不留存
date  source version num
2015-06-05    360    5.1.19.3962    1
2015-06-06    VZdfup    5.1.18.3909    1
2015-06-08    xl8    5.1.18.3909    2
2015-06-11    360    5.1.19.3962    1
2015-06-12    360    5.1.20.4010    1
2015-06-13    www    5.1.19.3962    1
2015-06-14    kkweb    5.1.18.3909    1
'''


#计算渠道留存率，但以peerid计算计量大于1
#一天各版本留存数和安装总数的计算
sel_sql='''
insert into result_source_remain_table(sta_date,sta_source,clc_num)  select sta_date,sta_source,count(*) from \
(select * from  mid_table where num>1) as sub1 group by sta_date,sta_source order by sta_date;

insert into result_source_remain_table(clc_totalnum) \
 select count(*) from mid_table group by sta_date,sta_source order by sta_date;
'''
cur.execute(sel_sql)
conn.commit()

#一天各渠道版本留存数和安装总数的计算
#数据入库
sel_sql='''
insert into result_version_remain_table(sta_date,sta_source,clc_num)  select sta_date,sta_source,count(*) from \
(select * from  mid_table where num>1) as sub1 group by sta_date,sta_version order by sta_date;

insert into result_version_remain_table(clc_totalnum) \
 select count(*) from mid_table group by sta_date,sta_version order by sta_date;

'''
cur.execute(sel_sql)
conn.commit()

#按渠道计算留存率
sel_sql='insert into result_source_remain_table(clc_remain) select clc_num/clc_totalnum from result_source_remain_table'
cur.execute(sel_sql)
conn.commit()

#按版本计算留存率
sel_sql='insert into result_version_remain_table(clc_remain) select clc_num/clc_totalnum from result_version_remain_table'
cur.execute(sel_sql)
conn.commit()


if __name__ == "__main__":
    pass
