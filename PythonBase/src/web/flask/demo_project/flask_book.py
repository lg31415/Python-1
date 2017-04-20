#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:flask演示添加书籍列表的方法
	Ref:head-first-python蓝图部分
	State：进行中
	Date:2017/4/20
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, request, redirect, url_for
app = Flask(__name__)
app.secret_key = 'some secret key'
books = ['the first book', 'the second book', 'the third book']
movies=['movie1','movie2','movie3']


# 查看书籍
@app.route("/")
def index():
	render_string = '<ul>'
	render_string += '<li><a href="http://localhost:5200/book">book</a></li>'
	render_string += '<li><a href="http://localhost:5200/movie">movie</a></li>'
	render_string += '</ul>'
	return render_string


# 如果是post方法则添加书籍并返回结果，如果是get方法，则显示添加书籍的页面
@app.route("/book", methods=['POST', 'GET'])
def book():
	_form = request.form
	if request.method == 'POST':
		title = _form["title"]
		books.append(title)
		return redirect(url_for('index'))
	else:
		result_list = '<ul>'
		for book in books:
			result_list += '<li>' + book + '</li>'
		result_list += '</ul>'

		form_book='''
		<form name="book" action="/book" method="post">
		<input id="title" name="title" type="text" placeholder="请输入书籍名">
		<button type="submit">Submit</button>
		</form>
		'''

		return result_list+"<hr/>"+form_book






if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5200, debug=True)
else:
	application=app.wsgi_app()


