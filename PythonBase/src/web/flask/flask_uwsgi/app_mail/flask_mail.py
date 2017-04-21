#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:flask邮件发送
	Ref:https://funhacks.gitbooks.io/head-first-flask/content/chapter03/section3.01.html
	State：
	Date:2017/4/21
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask_mail import Mail, Message
from threading import Thread
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.163.com'  # 邮件服务器地址
app.config['MAIL_PORT'] = 25 			    # 邮件服务器端口
app.config['MAIL_USE_TLS'] = True 			# 启用 TLS
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'username@163.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'mpassword'
mail = Mail(app)


@app.route('/')
def index():
	return "利用flask发送邮件"

'''
	同步发送邮件
'''
#同步发送邮件
@app.route('/sync')
def send_mail_sync():
	msg = Message('这是邮件的标题', sender='username@163.com', recipients=['xxxx@126.com'])
	# 富文本邮件
	msg.html = '<h2>这是邮件的大纲标题</h2><p>这是邮件的正文</p>'
	# 好像不支持表单数据
	msg.html+='''
		<form name="book" action="/book" method="post">
		<input id="title" name="title" type="text" placeholder="请输入书籍名">
		<button type="submit">Submit</button>
		</form>
	'''
	# 纯文本邮件
	#msg.body = 'The first email!'

	# 添加附件
	with app.open_resource("/Users/Admin/Documents/pixel-example.jpg") as fp:
		msg.attach("photo.jpg", "image/jpeg", fp.read())

	mail.send(msg)
	return '<h3>同步发送邮件发送成功,OK!</h3>'

'''
	异步发送邮件
'''
# 异步发送邮件
def send_async(app,msg):
	with app.app_context():
		mail.send(msg)

@app.route('/async')
def send_mail_async():
	msg = Message('这是异步发送邮件的标题', sender='username@163.com', recipients=['xxxx@126.com'])
	# 富文本邮件
	msg.html = '''<h2>大纲标题1</h2>
				 	<p>邮件正文1</p>
				  <h2>大纲标题2</h2>
				  	<p>邮件正文2</p>'''
	thr = Thread(target=send_async, args=[app, msg])
	thr.start()
	return '<h3>异步发送邮件发送成功,OK!</h3>'


#测试入口
if __name__ == '__main__':
	app.run(host='127.0.0.1',port=5200,debug=True)



