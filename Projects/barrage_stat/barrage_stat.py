#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
'''
	Fun:弹幕数据统计
	Ref:
	State：
	Date:2016/12/21
	Author:tuling56
'''
import os, sys
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
import json

reload(sys)
sys.setdefaultencoding('utf-8')

file_path = os.getcwd()

'''
	日志分割并构建pandas数据结构保存(tw07143端处理）
	注意这里采用了文件的方式进行保存，而不是pd自带的保存函数
'''
def log_split(log,proc_log):
	category_num = {}
	flog_proc = open(proc_log, 'w')
	print >> flog_proc, ','.join(["category", "groupID", "type", "key", "subkey", "peerid", "userid", "action", "title"])
	with open(log, "r") as f:
		for line in f:
			data_set = {"category": "", "groupID": "", "type": "", "key": "", "subkey": "", "peerid": "", "userid": "","action": "", "title": ""}  # 每一行都要创建新字典
			try:
				line = line.strip().split('\"')
				if not line: continue
				category, info = line[1].split('?')
				category = category.split()[1].replace('/', '')
				data_set["category"] = category
				# 类别汇总
				try:
					category_num[category] = category_num[category] + 1
				except:
					category_num[category] = 0

				if not info: continue
				infolist = info.split("&")
				for i in range(0, len(infolist)):
					if (len(infolist[i]) > 0) and infolist[i].find('=') != -1:
						key, value = infolist[i].split("=")
						if key in data_set:
							data_set[key] = value
				list_res = [data_set["category"], data_set["groupID"], data_set["type"], data_set["key"],
							data_set["subkey"], data_set["peerid"], data_set["userid"], data_set["action"],
							data_set["title"]]
				print >> flog_proc, ','.join(list(map(lambda x: str(x), list_res)))
			except Exception, e:
				# t,value,traceback = sys.exc_info()
				#print str(e)
				print "\033[1;31m%s\033[0m" % (line)
	print category_num




'''
	数据统计（利用pandas自带的groupby函数）
	输入：同步过来处理之后的csv文件
	输出：数据统计的结果Execl
'''
def data_stat_pandasby(flog_proc,outstat):
	pass



'''
	数据统计（对pandas数据结构进行汇总,利用pandassql实现）【tw07562端处理】
	输入：同步过来处理之后的csv文件
	输出：数据统计的结果Execl
'''
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())
def data_stat_pandasql(flog_proc):
	pdata = pd.read_csv(flog_proc,header=0,dtype=[''])
	#pdata.columns=["category", "groupID", "type", "key", "subkey", "peerid", "userid", "action", "title"]
	# 此处需要一个apply函数实现
	#pdata['dkey']=pdata['key']+pdata['subkey']   #组合新key，若有groupID则groupID为key，若没有则key+subkey为key
	pdata['dkey'] = pdata.apply(lambda x: x['groupID']+"1" if x['groupID'] else x['key'] + x['subkey'], axis=1)
	print pdata['dkey']
	print pdata
	return  0

	# 获取弹幕ID
	print "GetID:"
	getID_stat = pysqldf("select \"%s\" ,\"getID\",type,count(*) ,count(DISTINCT dkey)  from pdata where category=\"getID\";" % (calcday))

	# 统计下载弹幕次数和影片数
	print "下载:"
	down_stat = pysqldf("select \"%s\" ,\"download\",type,count(*) ,count(DISTINCT dkey)  from pdata where category=\"info\";" % (calcday))

	# 统计上报弹幕的次数，人数，影片数
	print "上报:"
	upload_stat = pysqldf("select \"%s\",\"upload\",type,count(*),count(distinct peerid),count(DISTINCT dkey) from pdata where category=\"upload\" GROUP by category,type;" % (calcday))

	# 统计点评弹幕的次数，影片数,（细分点赞和举报）
	print "点评:"
	remark_stat = pysqldf("select \"%s\",\"remark\",action,count(*),count(DISTINCT dkey) from pdata where category=\"remark\" GROUP by category,action;" % (calcday))

	# 统计搜索的次数,搜索的影片数
	print "搜索:"
	search_stat = pysqldf("select \"%s\",\"search\",count(*),count(DISTINCT title) from pdata where category=\"search\" GROUP by category;" % (calcday))

	#### 结果数据保存(csv测试)
	# down_stat.to_csv("hahh.csv",mode='a+',index=False,encoding='utf8')

	#### 结果数据保存Excel
	writer = pd.ExcelWriter(outstat)
	if not getID_stat.empty:
		getID_stat.columns = [u"日期", u"行为", u"影片类型", u"次数", u"影片数"]
		getID_stat.to_excel(writer, u'getID', index=False)
	#print down_stat
	if not down_stat.empty:
		down_stat.columns = [u"日期", u"行为", u"影片类型", u"次数", u"影片数"]
		down_stat.to_excel(writer, u'下载', index=False)
	#print down_stat
	if not upload_stat.empty:
		upload_stat.columns = [u"日期", u"行为", u"影片类型", u"次数", u"人数", u"影片数"]
		upload_stat.to_excel(writer, u'上报', index=False)
	#print upload_stat
	if not remark_stat.empty:
		remark_stat.columns = [u"日期", u"行为", u"动作", u"次数", u"影片数"]
		remark_stat.to_excel(writer, u'评论', index=False)
	#print remark_stat
	if not search_stat.empty:
		search_stat.columns = [u"日期", u"行为", u"影片类型", u"次数", u"影片数"]
		search_stat.to_excel(writer, u'搜索', index=False)
	#print search_stat
	writer.save()


'''
	数据统计（利用mysql）
	输入：同步过来处理之后的csv文件
	输出：数据统计的结果Execl
'''
import MySQLdb
def data_stat_mysql(flog_proc):
	detail_stat=os.path.join(file_path,"data","barrage_stat_detail_"+calcday)
	f=open(detail_stat,'w')
	try:
		conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='sd-9898w',db='test')
		cur=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		# 创建表和加载数据
		csql="use test;create table if not exists barrage_stat(category varchar(10), groupID varchar(30), type varchar(10), \`key\` varchar(100), subkey varchar(30), peerid varchar(20), userid varchar(30), action varchar(10), title varchar(50))ENGINE=MyISAM DEFAULT CHARSET=utf8;;"
		cur.execute(csql)
		lsql="use test;delete from barrage_stat;load data local infile '%s' into table barrage_stat fields terminated by ',';" %(flog_proc)
		cur.execute(lsql)
		conn.commit()
	except Exception,e:
		t,value,traceback = sys.exc_info()
		print str(e)

	#　利用mysql进行数据统计
	## 获取弹幕ID
	print "GetID:"
	qsql="select \"%s\" ,\"getID\",type,count(*) as '次数',count(DISTINCT groupID)+count(DISTINCT concat(`key`,subkey)) as '影片数' from test.barrage_stat where category=\"getID\";" % (calcday)
	print qsql
	cur.execute(qsql)
	data=cur.fetchall()
	json.dump(data,f)

	## 统计下载弹幕次数和影片数
	print "下载:"
	qsql="select \"%s\" ,\"download\",type,count(*) as '次数',count(DISTINCT groupID)+count(DISTINCT concat(`key`,subkey)) as '影片数'  from test.barrage_stat where category=\"info\";" % (calcday)
	print qsql
	cur.execute(qsql)
	data=cur.fetchall()
	json.dump(data,f)

	## 统计上报弹幕的次数，人数，影片数
	print "上报:"
	qsql="select \"%s\",\"upload\",type,count(*) as '次数',count(distinct peerid) as '人数',count(DISTINCT groupID)+count(DISTINCT concat(`key`,subkey)) as '影片数' from test.barrage_stat where category=\"upload\" GROUP by category,type;" % (calcday)
	print qsql
	cur.execute(qsql)
	data=cur.fetchall()
	json.dump(data,f)

	## 统计点评弹幕的次数，影片数,（细分点赞和举报）
	print "点评:"
	qsql="select \"%s\",\"remark\",action,count(*) as '次数',count(DISTINCT groupID)+count(DISTINCT concat(`key`,subkey)) as '影片数' from test.barrage_stat where category=\"remark\" GROUP by category,action;" % (calcday)
	print qsql
	cur.execute(qsql)
	data=cur.fetchall()
	json.dump(data,f)

	## 统计搜索的次数,搜索的影片数
	print "搜索:"
	qsql="select \"%s\",\"search\",count(*),count(DISTINCT title) from test.barrage_stat where category=\"search\" GROUP by category;" % (calcday)
	print qsql
	cur.execute(qsql)
	data=cur.fetchall()
	json.dump(data,f)
	#写入中文的时候用下面的方法
	#f.write(json.dumps(data,ensure_ascii=False)+"\n")

	conn.close()
	f.close()


'''
	数据统计（利用sqlite3）
	输入：同步过来处理之后的csv文件
	输出：数据统计的结果Execl
'''
def data_stat_sqlite3(flog_proc):
	pass


'''主体统计程序'''
if __name__ == "__main__":
	if len(sys.argv) <= 2:
		calcday = date.today() - timedelta(days=1)
		calcday = calcday.strftime("%Y%m%d")
		outstat = os.path.join(file_path, "barrage_stat_" + calcday)
	elif len(sys.argv) == 3:
		calcday = sys.argv[1]
		outstat = sys.argv[2]
	else:
		print '\033[1;31merror params num wrong,please use date as the paras\033[0m'
		exit()

	log_path = "/usr/local/nginx/logs/bak"
	log = os.path.join(log_path, "barrage_acc_" + calcday)
	log = "barrage_acc_20161222.log"
	proc_log="barrage_acc_20161222.proc.log"

	### 信息汇总
	print "[  InLog]:%s" % (log)
	print "[ProcLog]:%s" % (proc_log)
	print "[outstat]:%s" % (outstat)

	log_split(log,proc_log)
	data_stat_pandasql(proc_log)

