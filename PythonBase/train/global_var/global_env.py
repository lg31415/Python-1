#!/usr/bin/env python
# -*- coding: utf8 -*-
import os,sys

#环境变量和目录设置
try:
	if os.environ['KK_WORKSPACE'] is None:
		ENV_KK_WORKSPACE="."
	else:
		ENV_KK_WORKSPACE=os.environ['KK_WORKSPACE']
	common_dir=ENV_KK_WORKSPACE+"/bin/common"
	conf_dir=ENV_KK_WORKSPACE+"/conf"
except Exception,e:
	print str(e)

#命令行命令设置
SQOOP="/usr/local/complat/complat_clients/cli_bin/sqoop"
HIVE="/usr/local/complat/complat_clients/cli_bin/hive " \
	 "-hiveconf mapred.job.name=kkstat_hive -hiveconf " \
	 "hive.exec.compress.output=true " \
	 "-hiveconf hive.exec.compress.intermediate=true " \
	 "-hiveconf io.seqfile.compression.type=BLOCK " \
	 "-hiveconf mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec " \
	 "-hiveconf hive.map.aggr=true " \
	 "-hiveconf hive.stats.autogather=false " \
	 "-hiveconf hive.exec.scratchdir=/user/kankan/tmp " \
	 "-hiveconf mapred.job.queue.name=kankan  -S -e"
HADOOP="/usr/local/complat/complat_clients/cli_bin/hadoop" 

# 常用操作变量化
UDFLIB="add jar /usr/local/sandai/server/bin/jar/xl.kk.feature.udf.jar;add jar /usr/local/sandai/server/bin/jar/com.xunlei.kk.feature.udf.jar;"
UDF_CREATE="create temporary function uridecode as 'com.xunlei.kk.feature.udf.UDFURIDecoder';create temporary function uriencode as 'com.xunlei.kk.feature.udf.UDFURIEncoder';"

#配置文件模块化
import MySQLdb
from ConfigParser import RawConfigParser

MYSQL93="/usr/bin/mysql -h10.65.1.196 -uroot -psd-9898w -N -e"
MYSQL94="/usr/bin/mysql -uroot -psd-9898w -h10.1.1.194 -N -e"
MYSQL10="/usr/bin/mysql -uroot -phive -N -e"
MYSQL="/usr/bin/mysql -uroot -phive -N -e"

config = None
def load_config():
	global config
	config = RawConfigParser()
	ret = config.read(conf_dir+"/mysql.ini")
	if 0 == ret:
		print >> sys.stderr,"read config err"

def open(machine):
	__user = config.get(machine,'user')
	__passwd = config.get(machine,'psd')
	__host = config.get(machine,'host')
	conn = MySQLdb.connect(host=__host, user=__user,passwd=__passwd,charset='utf8')
	cursor = conn.cursor()
	return (conn,cursor)

def close(conn,cursor):
	cursor.close()
	conn.close()

if __name__=="__main__":
	print HIVE