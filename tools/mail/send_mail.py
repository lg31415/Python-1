#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
   发送带附近邮件类
'''
import sys,os
import re
import socket

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import date, datetime, timedelta

reload(sys)
sys.setdefaultencoding("utf-8")

yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%Y%m%d")


class SendMail():
    def __init__(self):
        #创建一个带附件的实例
        self.msg = MIMEMultipart()
        self.msg['from'] = 'monitor@cc.sandai.net'
        self.hostname=socket.gethostname()
    def setattach(self,attach_name):
        size = os.popen("du -h %s | awk '{print $1}'" % attach_name)
        size=re.search('\d+',size.read()).group(0)
        #print size
        if int(size) ==0:
            print '\033[1;31mfile size error!\033[0m'
            print attach_name,"\t[size]:",size
            return 1
        #构造附件1
        att1 = MIMEText(open(attach_name, 'rb').read(), 'base64', 'gb2312')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="%s"' % (os.path.basename(attach_name))
        self.msg.attach(att1)
    
    def settocopy(self,tolist,copylist=['server','xmp']):
        serverlist=['luochuan@cc.sandai.net','liuyinfeng@cc.sandai.net','yuanjunmiao@cc.sandai.net','maohaibo@cc.sandai.net']
        xmplist=['lizhi@cc.sandai.net','zhanghaobo@cc.sandai.net','yinqiulai@cc.sandai.net']
        if 'server' in copylist:
            copylist.remove('server')
            copylist.extend(serverlist)
        if 'xmp' in copylist:
            copylist.remove('xmp')
            copylist.extend(xmplist)
        self.msg['to'] = ','.join(tolist)
        if copylist:
            self.msg['Cc'] = ','.join(copylist)
            #print "[翻译后的抄送人]:",self.msg['Cc']
    
    def settitle(self,title):
        subject = title
        self.msg['subject'] = unicode(subject.decode('utf8'))
    
    #添加邮件内容
    def setbody(self,body):    
        content=body
        content = MIMEText(unicode(content.decode('utf-8')), "plain", "utf-8")
        self.msg.attach(content)
    
    #发送邮件
    def send(self):
        try:
            server = smtplib.SMTP()
            #server.set_debuglevel(1)
            server.connect('mail.cc.sandai.net')
            server.login('monitor@cc.sandai.net','121212')
            server.sendmail(self.msg['from'], self.msg['to'],self.msg.as_string())
            server.quit()
            print '\033[1;31m发送成功!\033[0m'
        except Exception, e:  
            print str(e)

#简单的邮件过期报警
class SendWarn():
    def __init__(self):
        self.to='yuanjunmiao@cc.sandai.net'
        self.title="关闭提醒".decode('utf8')
        self.attach=""
        self.hostname=socket.gethostname()
        self.mail='/usr/local/monitor-base/bin/sendEmail -s mail.cc.sandai.net -f monitor@cc.sandai.net -xu monitor@cc.sandai.net -xp 121212'
    def settitle(self,title):
        self.title=title
    def setattach(self,attach):
        self.attach=attach
    def setbody(self,body):
        self.body=body
    def send(self):
        shellsend="%s -t '%s' -u '%s' -m '%s' -a '%s'" %(self.mail,self.to,self.title,self.body,self.attach)
        if os.system(shellsend)!=0:
            print "send mail fail"
        else:
            print "send mail sucess"


if __name__=="__main__":
    sendm=SendMail()
    sendm.settocopy(['yuanjunmiao@cc.sandai.net'])
    sendm.settitle(yesterday+'张先生你好')
    sendm.setbody('这是邮件内容')
    sendm.setattach('test.txt')
    sendm.send()
