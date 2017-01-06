#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:http://www.pythondoc.com/flask/quickstart.html#id2
	State：
	Date:2016/11/14
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Flask
app = Flask(__name__)
app.debug = True

# 路由映射
@app.route('/')
def index():
    return 'Hello Flask!'

@app.route('/add/')
def add_num():
    return 'this is add num!'

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5500,debug=True)
