#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:
	State：
	Date:2016/11/17
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


from blog_app1 import db
class User(db.Model):
	__tablename__ = 'b_user'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(10),unique=True)
	password = db.Column(db.String(16))
	def __init__(self,username,password):
		self.username = username
		self.password = password
	def __repr__(self):
		return '<User %r>' % self.username

if __name__ == "__main__":
	fun()

