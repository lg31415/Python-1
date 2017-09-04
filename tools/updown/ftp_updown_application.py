#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:ftp文件上传和下载
    Ref:http://blog.csdn.net/linda1000/article/details/8255771
    State：
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
        self.bufsize=1024                   # 设置的缓冲区大小
        timeout = 30
        port =21
        self.ftp = FTP()
        try:
            #self.ftp.set_debuglevel(2)          # 打开调试级别2，显示详细信息
            self.ftp.set_pasv(1)                 # 0是主动模式，1是被动模式
            self.ftp.connect(host,port,timeout)  # 连接FTP服务器
            self.ftp.login('bxu2713660548','yunosa112233')       # 登录
            self.ftp.cwd('/htdocs')
            self.ftp.dir()
            print self.ftp.getwelcome()          # 获得欢迎信息
        except Exception,e:
            hues.error("登录失败:",str(e))
            sys.exit(1)
        else:
            hues.success("登录成功")

    def __del__(self):
        try:
            #self.ftp.set_debuglevel(0)          # 关闭调试模式
            #self.ftp.close()
            self.ftp.quit()                     # 退出FTP服务器
        except Exception,e:
            hues.warn("关闭连接时候出错:",str(e))

    def __proc_time(self,tstr):
        if ':' in tstr:
            tstr=str(date.today().year)+" "+tstr
            timeArray=time.strptime(tstr,'%Y %b %d %H:%M')
        else:
            timeArray=time.strptime(tstr,'%b %d %Y')
        timeStamp=int(time.mktime(timeArray))   #日期时间结构体转时间戳
        return timeStamp


    def __line_proc( self, line):
        infolist=line.split()
        fdir=infolist[0]
        fsize=infolist[-5]
        ffile=infolist[-1]
        if fdir.startswith('d'):
            print "目录:",ffile
        else:
            print "文件:",ffile
            ftime_str=' '.join(infolist[-4:-1]) #这里需要个转换操作
            ftime_stamp=self.__proc_time(ftime_str)


    # 获取文件列表
    def getlist(self,remote_path='./'):
        self.ftp.cwd(remote_path)            # 设置FTP路径
        list=self.ftp.retrlines('LIST',self.__line_proc)      # 获得目录列表(直接在控制台输出了。。。)
        #list=self.ftp.sendcmd('DIR')        # 获得目录列表
        for name in list:
            print(name)                     # 打印文件名字

    # 下载文件
    def download_file(self,filename,local_path='./',remote_path='./'):
        self.ftp.cwd(remote_path)
        print "curdir:",self.ftp.pwd()
        filename=os.path.join(local_path,filename)
        with open(filename,'wb') as f:
            cmd = 'RETR %s' %(os.path.basename(filename))             # 保存FTP文件(其中的RETR命令是关键字，不可改变)
            self.ftp.retrbinary(cmd,f.write)                          # 保存FTP文件

    # 上传文件
    def upload_file(self,filename,local_path='./',remote_path='./'):
        self.ftp.cwd(remote_path)
        try:
            remote_size=self.ftp.size(filename) #获取文件大小可能失败
        except Exception,e:
            remote_size=0
        filename=os.path.join(local_path,filename)
        local_size=os.path.getsize(filename)
        if int(local_size)<=int(remote_size):
            isoverlap=raw_input("本地文件大小>远程ftp文件，确认覆盖Y/N")
            if isoverlap=='Y':
                hues.warn("覆盖远程文件")
            else:
                return
        with open(filename, 'rb') as f:
            cmd='STOR %s ' %(os.path.basename(filename))
            self.ftp.storbinary(cmd,f,self.bufsize,rest=None) # 上传FTP文件（其中的STOR是关键字，不可改变）

    # 下载文件夹
    def download_dir(self,local_dir, remote_dir):
        if not os.path.isdir(local_dir):
           os.makedirs(local_dir)
        self.ftp.cwd(remote_dir)
        RemoteNames = self.ftp.nlst()
        for file in RemoteNames:
           Local = os.path.join(local_dir, file )
           if self._isDir( file ):
              self.download_dir( Local, file )
           else:
              self.download_file(Local, file )
        self.ftp.cwd( ".." )
        return


# 测试入口
if __name__ == "__main__":
    cftp=CFTP()
    cftp.getlist()
    #cftp.download_file('zhuye.html')
    #cftp.upload_file("README.md")


