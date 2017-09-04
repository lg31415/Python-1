#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:Pycurl模块的使用
    Ref:http://www.jb51.net/article/74840.htm
    State：
    Date:2017/9/1
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import pycurl
import StringIO

class CPyCurl(object):
    def __init__(self):
        self.is_gzip=0

    def _send_http_get(self,url, header = []):
        b = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, str(url))
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION,1)
        c.setopt(pycurl.MAXREDIRS,5)

        # cookie处理还有问题
        c.setopt(pycurl.COOKIE, )
        c.setopt(pycurl.COOKIEFILE, "cookie_file.ck")
        c.setopt(pycurl.COOKIEJAR, "cookie_jar.ck")
        c.setopt(pycurl.INFO_COOKIELIST)

        if len(header) > 0:
            c.setopt(pycurl.HTTPHEADER, header)

        if self.is_gzip == 1:
            c.setopt(pycurl.ENCODING, 'gzip')

        c.perform()
        status = c.getinfo(pycurl.HTTP_CODE)
        return (status, b.getvalue())

# 测试入口
if __name__ == "__main__":
    mpc=CPyCurl()
    print mpc._send_http_get('http://www.baidu.com')

