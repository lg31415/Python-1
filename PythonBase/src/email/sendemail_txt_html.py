#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：发送邮件（txt格式和html格式）
  参考来源：http://www.cnblogs.com/liu-ke/p/4872195.html
             注意修改编码格式
'''
import smtplib
from email.mime.text import MIMEText

mailto_list=["873925609@qq.com"]
mail_host="smtp.163.com"  #设置服务器
mail_user="xxxxx"    #用户名
mail_pass="xxxxx"   #口令
mail_postfix="163.com"  #发件箱的后缀


#发送txt格式的邮件
def send_txt_mail(to_list,sub,content):
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='gbk2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # connect&&login
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string().encode('utf8'))
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


#发送html格式的邮件
def send_html_mail(to_list,sub,content):                         #to_list：收件人；sub：主题；content：邮件内容
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"                #这里的hello可以任意设置，收到信后，将按照设置显示
    print  me

    msg = MIMEText(content,_subtype='html',_charset='utf8')    #创建一个实例，这里设置为html格式邮件,邮件正文
    msg['Subject'] = sub    #设置主题
    msg['From'] = me        #邮件来自于
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)                      #连接smtp服务器
        s.login(mail_user,mail_pass)              #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件，me的设置有问题？
        s.close()                                 #发送完后关闭
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == '__main__':
    '''
    if send_htmlmail(mailto_list,"关于邮件的测试","<a href='http://www.baidu.com'>这是重要的内容</a>"):
        print "发送html邮件成功" ,mailto_list
    else:
        print "发送html失败"
    '''

    if send_html_mail(mailto_list,"以txt发送邮件内容的测试","这是txt邮件内容"):
        print "发送txt邮件成功" ,mailto_list
    else:
        print "发送txt失败"


