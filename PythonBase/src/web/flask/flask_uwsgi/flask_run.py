#!/usr/bin/env python
# encoding: utf-8
from flask import Flask,render_template
from app_book import book_bp
from app_movie import movie_bp

application = Flask(__name__)
application.secret_key='this is sercry code'

#注册蓝图
application.register_blueprint(book_bp)
application.register_blueprint(movie_bp)

# 首页
@application.route('/', methods=['GET'])
def index():
    #return '<h2>Hello flask,this is flask demo</h2>'
    return render_template('index.html')


# 找不到页面
@application.errorhandler(404)
def page_not_find(error):
    return render_template('404.html'),404

# 服务器内部错误
@application.errorhandler(403)
def server_error(error):
    return render_template('403.html'),403


# 测试入口
if __name__ == '__main__':
    #app.run(host = '127.0.0.1', port = 8100)
    application.run()
