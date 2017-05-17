#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:利用Jinja2实现模板的渲染
	Ref:http://docs.jinkan.org/docs/jinja2/api.html
	State：开发中
	Date:2017/5/17
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('yourapplication', 'templates'))

def render_table():
	pass


if __name__ == "__main__":
	render_table()

