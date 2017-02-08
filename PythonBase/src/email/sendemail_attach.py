#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：发送邮件+附件
  参考：http://python.jobbole.com/83719/
'''
import smtplib
import getopt
import sys
import os

#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email.MIMEText import MIMEText

#用下面的代替上面的导入语句
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import email.Encoders as encoders

from datetime import  date,timedelta

# 邮件主题
def send_mail(mail_from, mail_to, subject, msg_txt, files=[]):
    # 创建邮件
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = mail_to

    # Create the body of the message (a plain-text and an HTML version).
    #text = msg
    html = msg_txt

    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)

    #attachment(文件的编码问题没解决)
    for f in files:
        # octet-stream:binary data(有问题)
        '''
        part = MIMEApplication('application', 'octet-stream')
        part.set_payload(open(f, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
        '''
        # 文本数据流：
        fname=os.path.split(f)[1]
        att = MIMEText(open(f, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        # att["Content-Disposition"] = "attachment; filename='中文.txt'.decode('utf-8')"
        att["Content-Disposition"] ="attachment; filename='%s'"  %(fname)
        msg.attach(att)

    # 邮件服务器设置
    # sendmail function takes 3 arguments: sender's address, recipient's address and message to send - here it is sent as one string.
    mail_host="smtp.163.com"    #设置服务器
    mail_user="yueqiulaishu"    #用户名
    mail_pass="yjm112233"       #口令
    s = smtplib.SMTP(mail_host)
    s.login(mail_user,mail_pass)

    #发送邮件
    mailto_list = mail_to.strip().split(",")
    if len(mailto_list) > 1:
        for mailtoi in mailto_list:
            s.sendmail(mail_from, mailtoi.strip(), msg.as_string())
    else:
        s.sendmail(mail_from, mail_to, msg.as_string())
    s.quit()
    return True


# 测试主体
def main():
    # 命令行参数解析
    files = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:t:s:m:a:")
        for op, value in opts:
            if op == "-f":
                mail_from = value
            elif op == "-t":
                mail_to = value
            elif op == "-s":
                subject = value
            elif op == "-m":
                msg_txt = value
            elif op == "-a":
                files = value.split(",")
    except getopt.GetoptError:
        print(sys.argv[0] + " : params are not defined well!")

    # 手动设置
    mail_from='yueqiulaishu@163.com'
    mail_to="873925609@qq.com"
    subject="主题:数据异常报警"
    msg_txt="正文:数据导入失败"

    #files=["../../data/bin.png","../../data/file_a.txt"]

    # 结果存放目录
    yestoday = date.today() - timedelta(days=1)
    yestoday = yestoday.strftime("%Y%m%d")
    dstdir=os.path.join("C:\\Users\\yjm\\Desktop",yestoday)
    files=[]
    for file in os.listdir(dstdir):
        pfile=os.path.join(dstdir,file)
        if os.path.isfile(pfile):
            files.append(pfile)
            print pfile

    print mail_from, mail_to, subject, msg_txt

    if files:
        send_mail(mail_from, mail_to, subject, msg_txt, files)
    else:
        send_mail(mail_from, mail_to, subject, msg_txt)

if __name__ == "__main__":
    main()
