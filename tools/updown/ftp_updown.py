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

reload(sys)
sys.setdefaultencoding('utf-8')

from ftplib import FTP

class CFTP():
    def __init__(self,host='127.0.0.1'):
        self.bufsize=1024                   # 设置的缓冲区大小
        timeout = 30
        port =21
        self.ftp = FTP()
        try:
            #self.ftp.set_debuglevel(2)          # 打开调试级别2，显示详细信息
            self.ftp.set_pasv(0)                 # 0是主动模式，1是被动模式
            self.ftp.connect(host,port,timeout)  # 连接FTP服务器
            self.ftp.login('xl','a112233')       # 登录
            print self.ftp.getwelcome()          # 获得欢迎信息
        except Exception,e:
            print "登录失败:",str(e)
            sys.exit(1)

    def __del__(self):
        #self.ftp.set_debuglevel(0)          # 关闭调试模式
        self.ftp.close()
        self.ftp.quit()                     # 退出FTP服务器

    def getlist(self):
        self.ftp.cwd(r'/C:/Users/xl/Downloads/Compressed/12306Bypass/')    # 设置FTP路径
        list=self.ftp.retrlines('LIST')      # 获得目录列表(直接在控制台输出了。。。)
        list=self.ftp.sendcmd('DIR')        # 获得目录列表
        for name in list:
            print(name)             # 打印文件名字

    # 下载的这个已经完成
    def download(self,filename='xxx.out',remote_path='/D:/'):
        self.ftp.cwd(remote_path)
        with open(filename,'wb') as f:
            cmd = 'RETR ' + filename                                  # 保存FTP文件(其中的RETR命令是关键字，不可改变)
            self.ftp.retrbinary(cmd,f.write,self.bufsize,rest=None)   # 保存FTP上的文件



    # 上传还待测试
    def upload(self,filename,remote_path='/D:/'):
        self.ftp.cwd(remote_path)
        filename='README.md'
        with open(filename, 'rb') as f:
            cmd='STOR '+filename
            self.ftp.storbinary(cmd,f,self.bufsize,rest=None) # 上传FTP文件（其中的STOR是关键字，不可改变）



# 测试入口
if __name__ == "__main__":
    cftp=CFTP()
    cftp.getlist()
    #cftp.download()
    #cftp.upload("README.md")


