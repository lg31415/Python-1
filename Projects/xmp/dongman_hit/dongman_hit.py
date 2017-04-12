#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:动漫击中统计：1:从文件构造字典
	Ref:
	Date:2016/10/14
	Author:tuling56
'''
import os
import sys
import re
import json

reload(sys)
sys.setdefaultencoding('utf-8')


# 构造字典
names_id={}
def build_dict():
	print "\033[1;31m构造字典\033[0m"
	f=open("res_d1","w")
	sinfo=""
	with open(r"bangumi.txt",'r') as f:
		names=[]
		i=1
		for line in f:
			#print "[%s]:%4.2f" %(i,i*100.0/11298)
			i=i+1
			lres=line.decode('utf8').strip('\t').strip('\n').split("\t")
			if len(lres[1])!=0:
				names.append(lres[1])
			if len(lres[2])!=0:
				names.extend(lres[2].split('|'))
			names=filter(lambda x:len(x)>0,names)
			#print names
			for name in names:
				#print name,lres[0]
				names_id[name.encode('utf8')]=lres[0]
				sinfo+=str(lres[0])+"\t"+name.encode('utf8')+"\n"
	f.write(sinfo)
	f.close()
	

	#结果保存(字典)
	f=open("dmhit_res_dict","w")
	print names_id
	json.dump(names_id,f)
	f.close()

# 字典加载
def load_dict():
	print "\033[1;31m加载字典\033[0m"
	global names_id
	with open("dmhit_res_dict","r") as f:
		names_id=json.load(f)
	print names_id



#名字处理
def title_proc(title):
	print "\033[1;31m名字处理\033[0m"
	ntitle=os.path.splitext(title)[0] # 去掉后缀
	patern=re.compile(r'\[.*\]',re.I)
	pps=re.findall(patern,ntitle)
	for pp in pps:
		ntitle=ntitle.replace(pp,'')
	
	ntitle=ntitle.strip('.').split('.')[0]

	return ntitle



# 计算次数	
id_playnum={}
def calc_hit():
	print "\033[1;31m次数计算\033[0m"
	with open("local_play_20160925",'r') as f:
		i=1
		for line in f:
			print "%4.2f" %(i*100/8245014)
			line=line.decode('utf8').strip('\n').split('\t')
			if len(line)<4:
				print "wrong parse"
				continue
			title,num=line[2],line[3]
			ntitle=title_proc(title)
			i=i+1
			if len(ntitle)>0:
				if names_id.has_key(ntitle):
					if id_playnum.has_key(ntitle):
						id_playnum[names_id.get(ntitle)]+=int(num)
					else:
						id_playnum[names_id.get(ntitle)]=int(num)
	# 结果文件保存
	f=open("dmhit_res_play",'w')
	json.dump(id_playnum,f)
	f.close()

# 程序入口
if __name__ == "__main__":
	build_dict()
	#load_dict()
	#calc_hit()


