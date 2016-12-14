#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:
	State：
	Date:2016/11/17
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


SQLALCHEMY_TRACK_MODIFICATIONS = False #session必须要设置key
SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #mysql数据库连接信息,这里改为自己的账号
SQLALCHEMY_DATABASE_URI = "mysql://username:password@ip:port/dbname"

if __name__ == "__main__":
	print "配置文件，数据库用户名，密码等"


