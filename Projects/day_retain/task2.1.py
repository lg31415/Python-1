# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：日留存计算，分按渠道和按版本
'''

import pymysql
import sys

src_peerid_table="src_peerid_table"  #28天的安装数据（peerid,date,source,version）
src_online_table="src_online_table"  #某一天的在线数据（peerid）
temp_merge_table="temp_merge_table"  #中间表（数据合并使用）
result_source_remain_table="result_source_remain_table"      #结果表1:按渠道的日留存表
result_version_remain_table="result_version_remain_table"    #结果表2:按版本的日留存表

'''
  Part1: **********数据准备**************
'''

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='task2') #新建的数据库
if not conn.open:
    print('open %s db fail'%('task2'))
    sys.exit()
cur=conn.cursor()

'''
   Part2: **********指标计算************
'''

# 合并表temp_merge_table的生成（将一个表插入到另一个表)[此处是将在线表插入到peerid表]
merge_sql='insert into %s select * from %s' %(temp_merge_table,src_peerid_table)
cur.execute(merge_sql)
conn.commit()
print('-------src_peerid_table->temp_merge_table---------')

merge_sql='insert into %s(peerid) select * from %s' %(temp_merge_table,src_online_table)
cur.execute(merge_sql)
conn.commit()
print('-------src_online_table->temp_merge_table---------')


#temp_merge_table复制到mid_table,mid_table这个表的价值意义很大
merge_sql='create table if not exists mid_table ' \
          'select * from (select *,count(*) as num from temp_merge_table group by peerid) as subsel_1' \
          'where sta_date is not null order by sta_date'
cur.execute(merge_sql)
conn.commit()
print('-------temp_merge_table->mid_table create---------')

'''
mid_table表的数据格式
date  source version num
2015-06-05	360	5.1.19.3962	1
2015-06-06	VZdfup	5.1.18.3909	1
2015-06-08	xl8	5.1.18.3909	2
2015-06-11	360	5.1.19.3962	1
2015-06-12	360	5.1.20.4010	1
2015-06-13	www	5.1.19.3962	1
2015-06-14	kkweb	5.1.18.3909	1
'''


#计算渠道留存率，但以peerid计算计量大于1
#一天各版本留存数和安装总数的计算
sel_sql='''
insert into result_source_remain_table(sta_date,sta_source,clc_num)  select sta_date,sta_source,count(*) from \
(select * from  mid_table where num>1) as sub1 group by sta_source order by sta_date;

insert into result_source_remain_table(clc_totalnum) \
 select count(*) from mid_table group by sta_source order by sta_date;
'''
cur.execute(sel_sql)
conn.commit()
print('-------source_num_totalnum already---------')


#一天各版本留存数和安装总数的计算
sel_sql='''
insert into result_version_remain_table(sta_date,sta_source,clc_num)  select sta_date,sta_source,count(*) from \
(select * from  mid_table where num>1) as sub1 group by sta_version order by sta_date;

insert into result_version_remain_table(clc_totalnum) \
 select count(*) from mid_table group by sta_version order by sta_date;

'''
cur.execute(sel_sql)
conn.commit()
print('-------version_num_totalnum already---------')

#按渠道计算留存率
sel_sql='insert into result_source_remain_table(clc_remain) select clc_num/clc_totalnum from result_source_remain_table'
cur.execute(sel_sql)
conn.commit()
print('-------source_ratio already---------')

#按版本计算留存率
sel_sql='insert into result_version_remain_table(clc_remain) select clc_num/clc_totalnum from result_version_remain_table'
cur.execute(sel_sql)
conn.commit()
print('-------version_ratio already---------')

conn.close()

if __name__ == "__main__":
    pass
