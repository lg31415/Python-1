#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
   发送带附近邮件类
'''

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import sys,os
import re
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

	def setattach(self,attach_name):
		size = os.popen("du -h %s | awk '{print $1}'" % attach_name)
		size=re.search('\d+',size.read()).group(0)
		#print size
		if int(size) ==0:
			print 'file size error!'
			return 0
		#构造附件1
		att1 = MIMEText(open(attach_name, 'rb').read(), 'base64', 'gb2312')
		att1["Content-Type"] = 'application/octet-stream'
		att1["Content-Disposition"] = 'attachment; filename="%s"' % (os.path.basename(attach_name))
		self.msg.attach(att1)
	
	def settocopy(self,tolist,copylist=[]):
		self.msg['to'] = ','.join(tolist)
		if copylist:
			self.msg['Cc'] = ','.join(copylist)
	
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
			print '发送成功'
		except Exception, e:  
			print str(e)


if __name__=="__main__":
	sendm=SendMail()
	sendm.settocopy(['yuanjunmiao@cc.sandai.net'])
	sendm.settitle(yesterday+'张先生你好')
	sendm.setbody('这是邮件内容')
	sendm.setattach('test.txt')
	sendm.send()
