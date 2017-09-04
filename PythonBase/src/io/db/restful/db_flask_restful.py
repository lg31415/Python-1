#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:db数据库查询的restful接口实现
    Ref:https://flask-restless.readthedocs.io/en/stable/
        https://segmentfault.com/q/1010000008335958?_ea=1878275
    Author:tuling56
    Date: 2017年5月5日
'''
import os,sys
import time
from datetime import date, datetime, timedelta

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

import flask
import flask_sqlalchemy
import flask_restless

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/test.db'
db = flask_sqlalchemy.SQLAlchemy(app)


# Create your Flask-SQLALchemy models as usual but with the following
# restriction: they must have an __init__ method that accepts keyword
# arguments for all columns (the constructor in
# flask_sqlalchemy.SQLAlchemy.Model supplies such a method, so you
# don't need to declare a new one).
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)   # 主键用来搜素
    name = db.Column(db.Unicode)
    birth_date = db.Column(db.Date)     # 日期类型


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)   # 主键用来搜素
    title = db.Column(db.Unicode)
    published_at = db.Column(db.DateTime)       # 日期时间类型
    author_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    author = db.relationship(Person, backref=db.backref('articles',lazy='dynamic'))


# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Person, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Article, methods=['GET'])

# start the flask loop
app.run()
