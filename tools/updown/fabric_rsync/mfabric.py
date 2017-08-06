#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:使用Fabric模块编写的批量同步文件的python脚本
	Ref:http://www.toutiao.com/i6449256257931969037/
	State：
	Date:2017/8/4
	Author:tuling56
'''
import re, os, sys
import hues
from fabric.api import task,put
from fabric.colors import yellow,green
from fabric.context_managers import settings,env

reload(sys)
sys.setdefaultencoding('utf-8')


env.user='root'
env.hosts=['localhost','localhost'] # 同步多台主机的配置
env.ports=[122,123]
env.password=['123']

@task
def mfabric():
	print yellow("开始同步")
	with settings(warn_only=False):
		put("D:\\xxx.log","/home/yjm/")
		print green("同步成功")

for host,port in zip(env.hosts,env.ports):
	env.host_string=host
	env.port=port
	mfabric()

# 测试入口
if __name__ == "__main__":
	hues.info("fabric测试开始")

