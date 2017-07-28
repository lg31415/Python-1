#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:httplib模块的使用
	Ref:http://blog.csdn.net/five3/article/details/7078951
	State：
	Date:2017/7/28
	Author:tuling56
'''
import re, os, sys
import hues
import urllib
import httplib

reload(sys)
sys.setdefaultencoding('utf-8')


# 测试post上报
def sendhttp_post():
    data = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection('bugs.python.org')
    conn.request('POST', '/', data, headers)
    httpres = conn.getresponse()
    print httpres.status
    print httpres.reason
    print httpres.read()


# 测试入口
if __name__ == "__main__":
    sendhttp_post()

