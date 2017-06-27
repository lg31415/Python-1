#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:logging模块学习
	Ref:http://www.cnblogs.com/dkblog/archive/2011/08/26/2155018.html
	State：
	Date:2017/6/27
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import logging
import logging.config
from logging.handlers import  RotatingFileHandler


class Mlog(object):
	def __init__(self):
		logging.basicConfig(level=logging.DEBUG,
							format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
							datefmt='%Y%m%d %H:%M:%S',
							filename='myapp.log',
							filemode='w')
							#stream=sys.stdout)
	def __logroll(self):
		#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
		Rthandler = RotatingFileHandler('myapp_roll.log', maxBytes=10*1024*1024,backupCount=5)
		Rthandler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		Rthandler.setFormatter(formatter)
		logging.getLogger('').addHandler(Rthandler)

	def __logconsole(self):
		# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
		console = logging.StreamHandler()
		console.setLevel(logging.INFO)
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		console.setFormatter(formatter)
		logging.getLogger('').addHandler(console)

	def __logfile(self):
		logf=logging.FileHandler('xx.log')
		logf.setLevel(logging.WARN)
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		logf.setFormatter(formatter)
		logging.getLogger('').addHandler(logf)

	def __logconf(self):
		logging.config.fileConfig("logger.conf")
		logger = logging.getLogger("example01")

		logger.debug('This is debug message')
		logger.info('This is info message')
		logger.warning('This is warning message')


	def log(self):
		self.__logconf()
		return
		self.__logconsole()
		self.__logroll()
		self.__logfile()
		logging.debug('debug message')
		logging.info('info message')
		logging.warning('warning message')
		logging.error('error message')

# 测试入口
if __name__ == "__main__":
	mlog = Mlog()
	mlog.log()

