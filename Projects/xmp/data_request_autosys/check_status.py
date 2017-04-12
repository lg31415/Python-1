#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:检查业务状态配置，选择有效的业务进行执行,无效任务首次失效报警
	Ref:
	Date:2016/9/22
	Author:tuling56
'''
import os
import sys
import re
from datetime import date, datetime, timedelta

os.environ['DATA_ROOT']='/usr/local/data_request/'
DATA_ROOT=os.environ['DATA_ROOT']
bin_dir=DATA_ROOT+"bin"
conf_dir=DATA_ROOT+"conf"
comm_dir=DATA_ROOT+"common"
sys.path.append(comm_dir)

from send_mail import SendMail

reload(sys)
sys.setdefaultencoding('utf-8')

task_status=os.path.join(conf_dir,"task_status.txt")
task_config=os.path.join(conf_dir,"task_config.txt")

nowdate = date.today().strftime("%Y%m%d")
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%Y%m%d")

validtask={}
invalidtask={}
status_head=""
config_head=""

'''
	检查作业状态，生成有效作业
'''
def check_status():
	head=True
	with open(task_status) as f:
		for line in f:
			taskid,status,start_date,end_date,proposer,receiver=line.strip().split()
			print taskid,status,start_date,end_date,proposer,receiver
			if head:
				status_head=line
				#print "业务头:",status_head
				head=False
				continue
			if nowdate<end_date and status.strip()=="on":
				validtask[taskid]=[','.join([rep+'@cc.sandai.net' for rep in receiver.split(',')])]
			if nowdate==end_date and status.strip()=="on":
				invalidtask[taskid]=line
			#if nowdate<end_date and status.strip()=="off":
			#	invalidtask=invalidtask+line+"被手动关闭\r\n"
	head=True
	with open(task_config) as f:
		for line in f:
			taskid,scriptor,desccriptor=line.strip().split()
			if head:
				config_head=line
				#print "配置头:",config_head
				head=False
				continue
			if taskid in validtask.keys():
				validtask[taskid].append(scriptor)
			elif taskid in invalidtask.keys():
				invalidtask[taskid]="业务:%s 即将到期自动关闭!!!\r\n详细信息如下：\r\n%s%s" %(desccriptor,status_head,invalidtask[taskid])
			else:
				print "wrong task_config"
'''
	生成有效任务的运行脚本
'''
validrun=[]
def gen_valid_data():
	for value in validtask.values():
		print "[有效任务]:",value
		receiver,scriptor=value
		ext=os.path.splitext(scriptor)[1]
		run=""
		if ext=='.sh':
			run=" ".join(["sh",scriptor,yesterday])
			print run
		elif ext==".py":
			run=" ".join(["python",scriptor,yesterday])
			print run
		else:
			print "[wrong exectule file]",ext,scriptor
		if not run:
			print run
			validrun.append(run)
	#运行有效脚本
	for task in validrun:
		print "[执行任务:]",task
		#if(os.system(task))!=0:
		#	print "\033[31m%s执行失败\033[0m" %(task)

'''
	无效任务邮件报警（首次,只在任务即将过期时候报警）
'''
def gen_invalid_warn():
	warncontent="\r\n".join(invalidtask.values())
	sendm=SendMail()
	sendm.settitle("邮件关闭提醒")
	sendm.settocopy(['yuanjunmiao@cc.sandai.net'])
	body=warncontent+"\r\n当前的配置状态请查看附件;若不想关闭,请到%s修改%s\r\n,确保截止日期大于当前日期且设置开关状态为on\r\n" %(sendm.hostname,task_status)
	print body
	return 0
	sendm.setbody(body)
	sendm.setattach(task_status) # 发送当前的配置状态
	sendm.send()


'''
	程序主体
'''
if __name__ == "__main__":
	check_status()
	gen_valid_data()
	#gen_invalid_warn()

