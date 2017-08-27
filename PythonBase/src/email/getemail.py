#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：收取邮件并下载附件
'''

import os,sys
import poplib
import cStringIO
import email
from email.parser import Parser
import base64
from datetime import datetime,timedelta,date
import shutil

class CGetMail:
    def __init__(self):
        self.usename='yuanjunmiao'
        self.password='XLyjm7654'
        self._ready_dir()

    # 目录准备
    def _ready_dir(self):
        yestoday = date.today() - timedelta(days=1)
        yestoday = yestoday.strftime("%Y%m%d")
        today=date.today()
        today=today.strftime("%Y%m%d")
        self.todaydir=os.path.join("C:\\Users\\xl\\Desktop",today)
        self.yestodaydir=os.path.join("C:\\Users\\xl\\Desktop",yestoday)
        rootdir="E:\\XMP\\Record"
        monthdir=yestoday[0:6]
        dstdir=os.path.join(rootdir,monthdir)

        # 创建当天的目录
        if not os.path.exists(self.todaydir):
            os.mkdir(self.todaydir)
        else:
            print self.todaydir+"  exists"

        # 创建目的目录
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        try:
            shutil.move(self.yestodaydir,dstdir)
        except Exception,e:
            s=sys.exc_info()
            print str(e)

    # 测试还有问题
    def getm_1(self):
        msever=poplib.POP3('mail.cc.sandai.net')
        msever.user(self.usename)
        msever.pass_(self.password)
        numMessages=len(msever.list()[1])
        print 'num of messages',numMessages
        for i in range(numMessages):
            m = msever.retr(i+1)
            buf = cStringIO.StringIO()
            for item in Parser().parsestr("\n".join(m[1])):
                print >>buf,item
            buf.seek(0)
            #保存附件
            msg = email.message_from_file(buf)
            for part in msg.walk():
                contenttype = part.get_content_type()
                filename = part.get_filename()
                if filename and contenttype=='application/octet-stream':
                    f = open("mail%d.%s.attach" % (i+1,filename),'wb')
                    f.write(base64.decodestring(part.get_payload()))
                    f.close()
        msever.quit()

    # 测试成功
    def getm_2(self):
        todaydir=self._ready_dir()

        msever=poplib.POP3('mail.cc.sandai.net')
        msever.user(self.usename)
        msever.pass_(self.password)

        # Concat message pieces:（提取所有邮件的邮件原始内容）
        messages = [msever.retr(i) for i in range(5, len(msever.list()[1]) + 1)]
        messages = ["\n".join(mssg[1]) for mssg in messages]
        #print messages

        #Parse message into an email object:（邮件内容解析后存储）
        messages = [Parser().parsestr(mssg) for mssg in messages]

        mailnum = 0
        for message in messages:
            mailName = "%s/mail_%d.%s" % (self.todaydir,mailnum, message["Subject"])
            f = open(mailName + '.log', 'w')

            # 保存每封邮件邮件头
            if True:
                mailnum = mailnum + 1
                print >> f, "Date: ", message["Date"]
                print >> f, "From: ", message["From"]
                print >> f, "To: ", message["To"]
                print >> f, "Subject: ", message["Subject"]
                print >> f, "Data: "

            # 保存邮件附件(一个邮件可以有多个附件)
            attachnum = 0
            for part in message.walk():
                attachnum = attachnum + 1
                fileName = part.get_filename()  #获取附件名字
                contentType = part.get_content_type()
                # 保存附件(对每封)
                if fileName:
                    data = part.get_payload(decode=True)
                    fileName = "%s.%d.%s" % (self.todaydir+'\\Attach', mailnum, fileName)
                    fEx = open(fileName, 'wb')
                    fEx.write(data)
                    fEx.close()
                # 保存邮件的正文
                elif contentType == 'text/plain' or contentType == 'text/html':
                    data = part.get_payload(decode=True)
                    print >> f, data
            f.close()
        msever.quit()


#  测试入口
if __name__ == "__main__":
    mpop=CGetMail()
    mpop.getm_2()


