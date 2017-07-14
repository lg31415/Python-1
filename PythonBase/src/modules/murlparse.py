#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:url参数解析
	Ref:http://blog.csdn.net/acceptedxukai/article/details/8806204
		http://www.cnblogs.com/huangcong/archive/2011/08/31/2160633.html
	State：此处只是做个引子，内容的完善需要自己完成
	Date:2017/4/14
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


import urlparse

def murlparse():
	url = "https://www.google.com.hk:8080/home/search;12432?newwi.1.9.serpuc#1234"

  	# urlparse
	r = urlparse.urlparse(url)
	print r
	print r.port,r.hostname
	print r.geturl()

	# urlsplit
	r = urlparse.urlsplit(url)
	print r
	parts = ["http","www.facebook.com","/home/email","132","parts","md5=?"]
	print urlparse.urlunparse(parts)
	print urlparse.urlunsplit(parts[0:5])

	# urljoin
	base = "http://baidu.com/home"
	url = "index.html"
	print urlparse.urljoin(base, url)
	base = "http://baidu.com/home/action.jsp"
	url = "index.html"
	print urlparse.urljoin(base, url)
	base = "http://baidu.com/home/action.jsp"
	url = "/index.html"
	print urlparse.urljoin(base, url)
	base = "http://baidu.com/home/action.jsp"
	url = "../../index.html"
	print urlparse.urljoin(base, url)


if __name__ == "__main__":
	murlparse()

