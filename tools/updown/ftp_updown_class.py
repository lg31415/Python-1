#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:ftp上传和下载文件
    Ref:http://www.jb51.net/article/67150.htm
    Author:tuling56
    Date:
'''
import os,sys
import time
from datetime import date, datetime, timedelta

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')


from ctypes import *
import ftplib

class CFtp(object):
    ftp = ftplib.FTP()
    bIsDir = False
    path = ""

    def __init__(self, host,user,passwd,port='21'):
        #self.ftp.set_debuglevel(2) # 打开调试级别2，显示详细信息
        #self.ftp.set_pasv(0)       # 0主动模式 1 #被动模式
        self.ftp.connect( host, port )
        self.ftp.login( user, passwd )
        print self.ftp.getwelcome()
        self.ftp.cwd('D:')
        #self.ftp.dir()


    def __del__(self):
        #self.ftp.set_debuglevel(0)
        self.ftp.quit()

    def __show( self, list ):
        result = list.lower().split( " " )
        if self.path in result and "<dir>" in result:
           self.bIsDir = True

    def _isDir( self, path ):
        self.bIsDir = False
        self.path = path
        #this ues callback function ,that will change bIsDir value
        self.ftp.retrlines( 'LIST', self.__show )
        return self.bIsDir


    # 下载文件
    def DownLoadFile( self, LocalFile, RemoteFile ):
        file_handler = open( LocalFile, 'wb' )
        self.ftp.retrbinary( "RETR %s" %( RemoteFile ), file_handler.write )
        file_handler.close()
        return True

    # 上传文件
    def UpLoadFile( self, LocalFile, RemoteFile):
        if os.path.isfile( LocalFile ) == False:
            return False
        file_handler = open( LocalFile, "rb" )
        self.ftp.storbinary( 'STOR %s' % os.path.basename(RemoteFile), file_handler, 4096 )
        file_handler.close()
        return True

    # 上传文件夹
    def UpLoadFileTree( self, LocalDir, RemoteDir ):
        if os.path.isdir( LocalDir ) == False:
           return False
        LocalNames = os.listdir( LocalDir )
        print RemoteDir
        self.ftp.cwd( RemoteDir )
        for Local in LocalNames:
           src = os.path.join( LocalDir, Local)
           if os.path.isdir( src ):
              self.UpLoadFileTree( src, Local )
           else:
              self.UpLoadFile( src, Local )
        self.ftp.cwd( ".." )
        return

    # 下载文件夹
    def DownLoadFileTree( self, LocalDir, RemoteDir ):
        if os.path.isdir( LocalDir ) == False:
            os.makedirs( LocalDir )
        self.ftp.cwd( RemoteDir )
        RemoteNames = self.ftp.nlst()
        for file in RemoteNames:
            Local = os.path.join( LocalDir, file )
            if self._isDir( file ):
                self.DownLoadFileTree( Local, file )
            else:
                self.DownLoadFile( Local, file )
        self.ftp.cwd( ".." )
        return


# 测试入口
if __name__ == "__main__":
    ftp = CFtp('127.0.0.1','xl','a112233')
    #ftp.DownLoadFile('TEST.TXT', 'others\\runtime.log')#ok
    ftp.UpLoadFile('README.md', 'xx.md')#ok

    #ftp.DownLoadFileTree('bcd', 'others\\abc')#ok
    #ftp.UpLoadFileTree('aaa',"others\\" )

    print "ok!"

