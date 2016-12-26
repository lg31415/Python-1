#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:弹幕数据统计
	Ref:
	State：
	Date:2016/12/21
	Author:tuling56
'''
import re, os, sys
import hues
from datetime import date, datetime, timedelta
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')

file_path=os.getcwd()
data_path=file_path.replace("/bin","/data")

if len(sys.argv) <= 1:
	calcday = date.today() - timedelta(days=1)
	calcday = calcday.strftime("%Y%m%d")
elif len(sys.argv) == 2:
	calcday = sys.argv[1]
else:
	print '\033[1;31merror params num wrong,please use date as the paras\033[0m'
	exit()

log_path="/usr/local/nginx/logs/bak"
log=os.path.join(log_path,"barrage_acc_"+calcday)

#测试
log=r"hest11.log"

# 日志分割并构建pandas数据结构
def log_split():
	data_set={"category":"","groupID":"","type":"","key":"","subkey":"","peerid":"","userid":"","action":"","title":""}
	lists=[]
	with open(log,"r") as f:
		for line in f:
			try:
				line=line.strip().split('\"')
				category,info=line[1].split('?')
				infolist=info.split("&")
				for i in range(0,len(infolist)):
					if(len(infolist[i])>0) and infolist[i].find('=')!=-1:
						key,value=infolist[i].split("=")
						if key in data_set:
							data_set[key]=value
				data_set["category"]=category.split()[1].replace('/','')
				list_res=[data_set["category"],data_set["groupID"],data_set["type"],data_set["key"],data_set["subkey"],data_set["peerid"],data_set["userid"],data_set["action"],data_set["title"]]
				lists.append(list_res)
			except Exception,e:
				t,value,traceback = sys.exc_info()
				print str(e)
				print t,value
		pdata=pd.DataFrame(lists,columns=["category","groupID","type","key","subkey","peerid","userid","action","title"])
		# 数据在保存的时候空值的处理
		return pdata




'''
	数据统计（对pandas数据结构进行汇总,利用pandassql实现）
'''
from pandasql import sqldf
pysqldf=lambda q:sqldf(q,globals())
def data_stat_sql(pdata):
	#此处需要一个apply函数实现
	#pdata['dkey']=pdata['key']+pdata['subkey']   #组合新key，若有groupID则groupID为key，若没有则key+subkey为key
	pdata['dkey']=pdata.apply(lambda x:x['groupID'] if x['groupID'] else x['key']+x['subkey'],axis=1)

	# 统计下载弹幕次数和影片数
	down_stat=pysqldf("select \"%s\" ,\"download\",type,count(*) ,count(DISTINCT dkey)  from pdata where category=\"info\";" %(calcday))

	# 统计上报弹幕的次数，人数，影片数
	upload_stat=pysqldf("select \"%s\",\"upload\",type,count(*),count(distinct peerid),count(DISTINCT dkey) from pdata where category=\"upload\" GROUP by category,type;" %(calcday))

	# 统计点评弹幕的次数，影片数,（细分点赞和举报）
	remark_stat=pysqldf("select \"%s\",\"remark\",action,count(*),count(DISTINCT dkey) from pdata where category=\"remark\" GROUP by category,action;" %(calcday))

	# 统计搜索的次数,搜索的影片数
	search_stat=pysqldf("select \"%s\",\"search\",count(*),count(DISTINCT title) from pdata where category=\"search\" GROUP by category;")

	# xlwx测试
	writer=pd.ExcelWriter("res.xlsx")
	if not down_stat.empty:
		down_stat.columns=[u"日期",u"行为",u"影片类型",u"次数",u"影片数"]
		down_stat.to_excel(writer,u'下载',index=False)
		#print down_stat
	if not upload_stat.empty:
		upload_stat.columns=[u"日期",u"行为",u"影片类型",u"次数",u"人数",u"影片数"]
		down_stat.to_excel(writer,u'上报',index=False)
		#print upload_stat
	if not remark_stat.empty:
		remark_stat.columns=[u"日期",u"行为",u"动作",u"次数",u"影片数"]
		down_stat.to_excel(writer,u'评论',index=False)
		#print remark_stat
	if not search_stat.empty:
		search_stat.columns=[u"日期",u"行为",u"影片类型",u"次数",u"影片数"]
		down_stat.to_excel(writer,u'搜索',index=False)
		#print search_stat
	writer.save()

	#csv 测试（可以追加内容，也可以覆盖，使用ascii码可保证在windows上打开的时候没有乱码）
	down_stat.to_csv("hahh.csv",mode='a+',index=False,encoding='ascii')


if __name__ == "__main__":
	pdata=log_split()
	data_stat_sql(pdata)

