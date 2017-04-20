#!/usr/bin/env python
# encoding: utf-8
from flask import Flask,render_template
from app_book import book_bp
#from app_movie import movive_bp

application = Flask(__name__)
application.secret_key='this is sercry code'

#注册蓝图
application.register_blueprint(book_bp)

'''
@application.route('/')
def hello_world():
    return "hello flask,this is flask world"
'''

@application.errorhandler(404)
def page_not_find(error):
    return render_template('404.html'),404


# 测试入口
if __name__ == '__main__':
    #app.run(host = '127.0.0.1', port = 8100)
    application.run()
