#/usr/bin/python 
#-*-coding:utf8-*-
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
#from email import encoders
import smtplib 
import sys

mailhost="mail.cc.sandai.net"    #邮件服务器
mailname="monitor@cc.sandai.net" #用户名
mailpass="xxxx"                #密码

'''
mailto="xiabin@xunlei.com"
context="This is a test mail"
msg=MIMEText(context)
msg['Subject'] ="相关指标异常报警"
msg['From']="XIABIN"
msg['To']=mailto
msg['Date'] = formatdate(localtime=True)

send_smtp =smtplib.SMTP()
send_smtp.connect(mailhost)
send_smtp.login(mailname,mailpass)
'''

# 增强功能
'''
for key in mailinfo.keys():
    v='\n'.join(mailinfo[key])
    print emad[key],v
    context=v
    msg=MIMEText(context,_charset='utf-8')
    msg['Subject'] ="相关指标异常报警"
    msg['From']="monitor@cc.sandai.net"
    msg['To']=emad[key]
    msg['Date']= formatdate(localtime=True)
    send_smtp.sendmail("monitor@cc.sandai.net",emad[key],msg.as_string())
#send_smtp =smtplib.SMTP()
#send_smtp.connect(mailhost)
#send_smtp.login(mailname,mailpass)
#send_smtp.sendmail("monitor@cc.sandai.net", "xiabin@xunlei.com", msg.as_string())
send_smtp.close()
'''


#opfile=open(sys.argv[1],'r')
#opfile1=open(sys.argv[2],'r')

opfile=open('sendemail.list','r')
opfile1=open('user.list','r')

gp_members={}

# 文件1获取报警内容和发送的邮件组user.list
for line in opfile1:
    emailaddr=[]
        str= line.rstrip().split("\t")  
        name=str[1].rstrip().split("|")
        for n in name:
                emailaddr.append(n+"@xunlei.com")
        gp_members[str[0]]=emailaddr

mailinfo={}
context_group={}

#获取邮件和组(sendemail.list)
for line in opfile:
    str=line.rstrip().split("\t")
    if context_group.has_key(str[1]):
        context_group[str[1]].append(str[0]) #邮件组作为key,邮件内容作为value
    else:
        context_group[str[1]]=[]
        context_group[str[1]].append(str[0])


# 给组中的每个人发送报警邮件
for g in context_group:
    send_smtp =smtplib.SMTP()
    send_smtp.connect(mailhost)  #均采用了这种方式
    send_smtp.login(mailname,mailpass)

    mailto=[]
    gps=g.rstrip().split("|")
    for gp in gps:
        mailto+=gp_members[gp]
    context='\n'.join(context_group[g])

    print mailto,context

    # 邮件体
    mailto_list=','.join(mailto)
    msg=MIMEText(context,_charset='utf-8')
    msg['Subject'] ="相关指标异常报警"
    msg['To']=mailto_list
    msg['From']="monitor@cc.sandai.net"
    msg['Date']= formatdate(localtime=True) 

    # send_smtp.sendmail("monitor@cc.sandai.net",mailto,msg.as_string())
    send_smtp.quit()


