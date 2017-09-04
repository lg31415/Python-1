#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:zip模块内容获取，打包，解包
    Ref:http://python.jobbole.com/81519/
    State：
    Date:2016/12/27
    Author:tuling56
'''
import re, os, sys
import hues
import zipfile

reload(sys)
sys.setdefaultencoding('utf-8')

#获取压缩包里一个文档的基本信息
def base_info(zipInfo):
    print 'filename:', zipInfo.filename
    print 'date_time:', zipInfo.date_time
    print 'compress_type:', zipInfo.compress_type
    print 'comment:', zipInfo.comment
    print 'extra:', zipInfo.extra
    print 'create_system:', zipInfo.create_system
    print 'create_version:', zipInfo.create_version
    print 'extract_version:', zipInfo.extract_version
    print 'extract_version:', zipInfo.reserved
    print 'flag_bits:', zipInfo.flag_bits
    print 'volume:', zipInfo.volume
    print 'internal_attr:', zipInfo.internal_attr
    print 'external_attr:', zipInfo.external_attr
    print 'header_offset:', zipInfo.header_offset
    print 'CRC:', zipInfo.CRC
    print 'compress_size:', zipInfo.compress_size
    print 'file_size:', zipInfo.file_size

# 读取压缩包里一个文档的内容
def get_content(zipFile):
    data = zipFile.read('BugReport.xml')
    (lambda f, d: (f.write(d), f.close()))(open(r'd:/txt.xml', 'wb'), data)  #一行语句就完成了写文件操作。仔细琢磨哦~_~
    zipFile.close()


def mzip():
    file="../../data/25-008906DD-0184B13D-03D488BD.zip"
    zipFile = zipfile.ZipFile(file)
    print zipFile.printdir()
    zipInfo = zipFile.getinfo('BugReport.xml')  #获取知道了指定文件的内容
    get_content(zipFile)
    #base_info(zipInfo)
    zipFile.close()

if __name__ == "__main__":
    mzip()

