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


from blog2 import db
class Category(db.Model):
	__tablename__ = 'b_category'
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(20),unique=True)
	content = db.Column(db.String(100))
	def __init__(self,title,content):
		self.title = title
		self.content = content
	def __repr__(self):
		return '<Category %r>' % self.title

if __name__ == "__main__":
	fun()

