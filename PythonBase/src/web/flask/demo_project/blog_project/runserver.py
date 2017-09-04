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

from  blog_app1 import app


@app.route('/')
def hello_world():
    return 'Hello，this is',__file__

@app.route('/hello')
def hello():
    return "hello,this is runserver.py"



if __name__ == "__main__":
    app.run(debug=True)

