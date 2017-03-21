#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：全局工具类
'''

import os
import sys
import re

'''
    txt2xls
'''
import xlwt
class CTxt2XlS():
    def __init__(self,input):
        self.input=input
        self.output=os.path.splitext(input)[0]+'.xls'
        self.workbook=xlwt.Workbook()
    def setoutput(self,output):
        self.output=output
    def addpic(self):
        table=self.workbook.add_sheet('T1')
        title="合并标题".decode('utf8')
        rdata=range(1,10)
        table.write_merge(0,1,0,1,title)
        table.write(3,0,'hahh')
        table.insert_bitmap('../data/test.bmp',5,1,4,4,0.5,0.5)
    def addtxt(self):
        table=self.data.add_sheet('T2')
        f=open(self.input,'r')
        contents=f.read().decode('utf8').split('\n')
        #contents=f.readlines()
        for i,v in enumerate(contents):
            lcontent=v.strip().split('\t')
            for j,vv in enumerate(lcontent):
                if isinstance(vv,float):
                    table.write(i,j,vv)  #浮点数据可以以指定格式写入
                else:
                    table.write(i,j,vv)
        f.close()
    def convert(self):
        self.addtxt()
        self.workbook.save(self.output)


'''
    邮件发送
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
class CSendMail():
    def __init__(self,fcontentname,fattachname):
        self.content=fcontentname
        self.attach=fattachname
        self.to_list=['yuanjunmiao@cc.sandai.net'] #,'luochuan@cc.sandai.net', 'lizhi@cc.sandai.net','yuanjunmiao@cc.sandai.net']
        self.copy_list=['yinqiulai@cc.sandai.net']
    def setcontent(self,fcontentname):
        self.content=fcontentname
    def setattach(self,fattachname):
        self.attach=fattachname
    def send(self):
        #创建一个带附件的实例
        msg = MIMEMultipart()

        #构造附件1
        att1 = MIMEText(open(self.attach, 'rb').read(), 'base64', 'gb2312')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="%s"' % (os.path.basename(self.attach))
        msg.attach(att1)

        #加邮件头
        msg['to'] = ','.join(self.to_list)
        msg['from'] = 'monitor@cc.sandai.net'
        subject = 'xmp数据异常'
        msg['subject'] = unicode(subject.decode('utf8'))
        #msg['Cc'] = ','.join(self.copy_list)

        #添加邮件内容
        f=open(self.content)
        content=f.read()
        content+="\n详情请查看附件！"
        f.close()
        content = MIMEText(unicode(content.decode('utf-8')), "plain", "utf-8")
        msg.attach(content)

        #发送邮件
        try:
            server = smtplib.SMTP()
            #server.set_debuglevel(1)
            server.connect('mail.cc.sandai.net')
            server.login('monitor@cc.sandai.net','121212')
            server.sendmail(msg['from'], self.to_list,msg.as_string())
            server.quit()
            print '邮件发送成功'
        except Exception, e:
            print '邮件发送失败'
            print str(e)

'''
    路径和文件操作
'''
class CPathFile(object):
    def __init__(self,path):
        self.path=path
        self.filelist=[]

    #递归获取所有全路径文件
    def getFilelist(self):
        classes={}
        for root, dirs, files in os.walk(self.path):
            for file in files:
                mclass=re.split('\\\\',root)[-1]
                readfile= os.path.join(root, file)
                self.filelist.append(readfile)
                fname = os.path.split(readfile)
            mclass=re.split('\\\\',root)[-1]
            if len(files)!=0:
                classes[mclass]=len(files)
        print classes,"total:",len(self.filelist)

    #获取路径，文件名，文件扩展
    def getPathNameExt(self):
       pass

    #切换路径
    def chndir(self,n):
        npath=self.path.count(os.sep)
        if npath>n:
            print "n too large"
            return 0
        if os.path.isdir(self.path):
            print "you input a path"
            return self.path.rsplit(os.sep,n)
        if os.path.isfile(self.path):
            print "you input a path"
            return self.path.rsplit(os.sep,n+1)


'''
    系统基本信息:
    Ref:http://www.cnblogs.com/snow-backup/p/4151276.html
'''
import platform
class CSysInfo():
    def __init__(self):
        pass

    # 系统平台判定
    def judge_platform(self):
        systr=platform.system()
        if systr=="Windows":
            return "Windows"
        elif systr=="Linux":
            return "Linux"
        else:
            return "Other"


'''
    测试入口
'''
if __name__ == "__main__":
    cf=CPathFile(r'D:\cygwin64\home\yjm\data\subdir')
    cf.getFilelist()
