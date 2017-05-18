#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:利用Jinja2实现模板的渲染
	Ref:http://docs.jinkan.org/docs/jinja2/api.html
		http://blog.csdn.net/kuaileboy1989/article/details/44195863
	State：开发中
	Date:2017/5/17
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

from jinja2 import Environment,FileSystemLoader,PackageLoader,Template
from jinja2 import TemplateError,TemplateNotFound,UndefinedError,TemplateSyntaxError  #异常处理
#template=Template('Hello {{name}}')									  # 模板环境加载-字符串
#env = Environment(loader=PackageLoader('template_render', 'templates'))  # 模板环境加载-包
env=Environment(loader=FileSystemLoader('templates'))					  # 模板环境加载-本地文件
try:
	template=env.get_template('jinja2_template.html')
except TemplateNotFound,e:
	#raise TemplateNotFound(template)
	pass
except TemplateError,e:
	print str(e)



blist=['李白凤','王二小','张大锤','小二黑']
dt={'id':'zhang','cid':'girl','filesize':23323,'ext':'http://www.baidu.com','operate_num':66}
ld=[{'id':'zhang','cid':'girl','filesize':23323,'ext':'http://www.baidu.com','operate_num':66},{'id':'wang','cid':'boy','filesize':6666,'ext':'rmvb','operate_num':23}]

# 渲染入口
def render_table():
	htmlres=template.render(books=blist,dt=dt,ld=ld)	#比如传一个字典列表，如何将字典列表转化成表格的形式
	f=open('res/jinja2_res.html','w')
	f.write(htmlres)
	f.close()

if __name__ == "__main__":
	render_table()

