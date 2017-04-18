#!/usr/bin/env python
# encoding: utf-8
from flask import Flask,render_template
application = Flask(__name__)


@application.route('/')
def hello_world():
    return "hello flask,this is flask world"

@application.route("/<dy_route>")
def dy_route(dy_route):
    # 不使用模板的方法
    #return '<h3>Hello,%s,this is dy_route;</h3>'  %dy_route

    # 使用模板的方法
    #return render_template('index.html',name=dy_route)
    return render_template('base_son.html')



# 测试入口
if __name__ == '__main__':
    #app.run(host = '127.0.0.1', port = 8100)
    application.run()
