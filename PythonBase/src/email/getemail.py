#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：收取带附件的邮件
'''

import os,sys
import poplib
import cStringIO
import email
from email.parser import Parser
import base64
from datetime import datetime,timedelta,date
import shutil

class CPOP:
    def __init__(self):
        self.usename='yuanjunmiao'
        self.password='XLyjm7654'

    # 测试还有问题
    def mpop3_1(self):
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
    def mpop3_2(self):
        todaydir=self.dirclear()

        msever=poplib.POP3('mail.cc.sandai.net')
        msever.user(self.usename)
        msever.pass_(self.password)

        # Concat message pieces:（提取所有邮件的邮件原始内容）
        messages = [msever.retr(i) for i in range(5, len(msever.list()[1]) + 1)]
        messages = ["\n".join(mssg[1]) for mssg in messages]
        #print messages

        #Parse message into an email object:（邮件内容解析后存储）
        messages = [Parser().parsestr(mssg) for mssg in messages]

        i = 0
        for message in messages:
            mailName = "mail%d.%s" % (i, message["Subject"])
            # 保存每封邮件邮件头
            f = open(mailName + '.log', 'w');
            if True:
                i = i + 1
                print >> f, "Date: ", message["Date"]
                print >> f, "From: ", message["From"]
                print >> f, "To: ", message["To"]
                print >> f, "Subject: ", message["Subject"]
                print >> f, "Data: "

            # 保存邮件附件(一个邮件可以有多个附件)
            j = 0
            for part in message.walk():
                j = j + 1
                fileName = part.get_filename()  #获取附件名字
                contentType = part.get_content_type()
                # 保存附件(对每封)
                if fileName:
                    data = part.get_payload(decode=True)
                    fileName = "%s.%d.%s" % (todaydir+'\\Attach', j, fileName)
                    fEx = open(fileName, 'wb')
                    fEx.write(data)
                    fEx.close()
                #保存正文
                elif contentType == 'text/plain' or contentType == 'text/html':
                    data = part.get_payload(decode=True)
                    print >> f, data
            f.close()
        msever.quit()

    # 目录清理
    def dirclear(self):
        yestoday = date.today() - timedelta(days=1)
        yestoday = yestoday.strftime("%Y%m%d")
        today=date.today()
        today=today.strftime("%Y%m%d")
        todaydir=os.path.join("C:\\Users\\yjm\\Desktop",today)
        yestodaydir=os.path.join("C:\\Users\\yjm\\Desktop",yestoday)
        rootdir="E:\\XMP\\Record"
        monthdir=yestoday[0:6]
        dstdir=os.path.join(rootdir,monthdir)
        if not os.path.exists(todaydir):
            os.mkdir(todaydir)
        else:
            print todaydir+"  exists"
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        try:
            shutil.move(yestodaydir,dstdir)
        except Exception,e:
            s=sys.exc_info()
            print "\033[1;31m[error]:{}\n[line]:{}\033[0m".format(s[1],s[2].tblineno)

        return todaydir;


if __name__ == "__main__":
    mpop=CPOP()
    mpop.mpop3_2()


