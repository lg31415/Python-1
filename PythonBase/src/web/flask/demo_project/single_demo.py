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

from flask import Flask,render_template,request, session, redirect,url_for

# 创建flask应用
app = Flask(__name__,static_url_path="")
app.debug = True

# 路由映射
@app.route('/')
def index():
    return 'Hello Flask!'


# 参数获取
@app.route("/<name>")
def hello(name):
    if name == 'ethan':
        return "<h1>Hello, world!</h1> <h2>Hello, %s!</h2>" % name
    else:
        return "<h1>Hello, world!</h1> <h2>Hello, world!</h2>"

# 模板使用
@app.route('/template/<name>')
def hello_template(name):
    if name == 'ethan':
        return render_template('index.html', name=name)
    else:
        return render_template('index.html', name='world')

# 会话
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user']
        session['user'] = user_name
        return 'hello, ' + session['user']
    elif request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('index'))
        else:
            return render_template('index.html')

app.secret_key = '123456'

'''
    应用启动入口
'''
if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5500,debug=True)
