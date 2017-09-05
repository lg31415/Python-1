#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:ftp文件（夹）上传和下载
    Ref:http://blog.csdn.net/linda1000/article/details/8255771
    State：测试通过全部功能
    Date:2017/9/4
    Author:tuling56
'''
import re, os, sys
import hues
import time
from datetime import date,datetime

reload(sys)
sys.setdefaultencoding('utf-8')

from ftplib import FTP

class CFTP():
    def __init__(self,host='bxu2713660548.my3w.com'):
        self.bufsize=1024                         # 设置的缓冲区大小
        self.ftimedict={}
        self.ftp = FTP()
        try:
            #self.ftp.set_debuglevel(2)           # 打开调试级别2，显示详细信息
            self.ftp.set_pasv(1)                  # 0是主动模式，1是被动模式
            self.ftp.connect(host,21,timeout=30)
            self.ftp.login('xxxxx','xxxxx')
            self.ftp.cwd('/htdocs')
            print self.ftp.getwelcome()
        except Exception,e:
            hues.error("登录失败:",str(e))
            sys.exit(1)
        else:
            hues.success("登录成功")

    def __del__(self):
        try:
            #self.ftp.set_debuglevel(0)          # 关闭调试模式
            #self.ftp.close()
            self.ftp.quit()                      # 退出FTP服务器
        except Exception,e:
            hues.warn("关闭连接时候出错:",str(e))

    # 判断是否是目录
    def __show( self, list ):
        result = list.lower().split( " " )
        if self.path in result and result[0].startswith('d'):
           self.bIsDir = True

    def _isDir( self, path ):
        self.bIsDir = False
        self.path = path
        #this ues callback function ,that will change bIsDir value
        self.ftp.retrlines( 'LIST', self.__show )
        return self.bIsDir


    # 下载文件(localfile是带路径的，remotefile是不带路径的，切换过去)
    def download_file(self,local_file,remote_file):
        print "remote_curdir:",self.ftp.pwd()
        with open(local_file,'wb') as f:
            try:
                cmd = 'RETR %s' %(remote_file)
                self.ftp.retrbinary(cmd,f.write)
            except Exception,e:
                hues.error("下载文件%s失败:%s" %(remote_file,str(e)))


    # 上传文件(localfile是带路径的,remotefile是不带路径的，切换过去)
    def upload_file(self,local_file,remote_file):
        print "remote_curdir:",self.ftp.pwd()
        if not os.path.isfile(local_file):
            return False
        with open(local_file, 'rb') as f:
            try:
                cmd='STOR %s ' %(os.path.basename(remote_file))
                self.ftp.storbinary(cmd,f,self.bufsize)
            except Exception,e:
                hues.error("上传文件%s失败:%s" %(local_file,str(e)))


    # 下载文件夹(测试通过)
    def download_dir(self,local_dir, remote_dir):
        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)
        self.ftp.cwd(remote_dir)
        RemoteNames = self.ftp.nlst()    # 获取远程文件列表的方法
        for file in RemoteNames:
            Local = os.path.join(local_dir, file )
            if self._isDir(file):
                self.download_dir(Local,file)
            else:
                self.download_file(Local,file )
        self.ftp.cwd( ".." )
        return

    # 上传文件夹（测试通过）
    def upload_dir(self,local_dir,remote_dir):
        if not os.path.isdir(local_dir):
            return False
        LocalNames=os.listdir(local_dir)# 获取本地文件列表的方法
        print remote_dir
        self.ftp.mkd(remote_dir)
        self.ftp.cwd(remote_dir)
        for local in LocalNames:
            src=os.path.join(local_dir,local)
            if os.path.isdir(src):
                self.upload_dir(src,local)
            else:
                self.upload_file(src,local)
        self.ftp.cwd("..")
        return


# 测试入口
if __name__ == "__main__":
    cftp=CFTP()
    #cftp.download_file('zhuye.html')
    #cftp.upload_file("README.md")
    cftp.download_dir("trash","/htdocs/trash")
    #cftp.upload_dir('D:\\Trash\\data xwe',"/htdocs/trash")
