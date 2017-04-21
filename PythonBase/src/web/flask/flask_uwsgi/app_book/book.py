#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:flask蓝图的使用
	Ref:
	State：
	Date:2017/4/20
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Blueprint, url_for, render_template, request,flash, redirect
# 创建一个蓝图对象
book_bp = Blueprint('book',	__name__,template_folder='../templates',)
books = ['book1', 'book2', 'book3']


# 添加数据和获取书籍列表
@book_bp.route('/book', methods=['GET', 'POST'])
def show_book():
	_form = request.form
	if request.method == 'POST':
		title = _form["title"]
		books.append(title)
		flash("add book successfully!")
		return redirect(url_for('book.show_book'))
	return render_template('book.html',books=books)


#获取某一本书籍的详细信息
@book_bp.route('/book/<name>')
def get_book_info(name):
	book = [name]
	if name not in books:
		book = []
	return render_template('book.html',books=book)


