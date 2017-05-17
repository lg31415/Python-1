#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:利用web.py实现html渲染
	Ref:
	State：
	Date:2017/5/17
	Author:tuling56
'''
import re, os, sys
import hues
import time

reload(sys)
sys.setdefaultencoding('utf-8')

import web
render = web.template.render('./templates/')

'''
	功能集
'''
def add_div(d):
	return '<div class="table table-condensed">{0}</div>'.format(str(d))

def add_tb(d):
	return '<table class="table table-hover">{0}</table>'.format(str(d))

def add_td(d):
	if 'http' in str(d):
		d='<a href="%s">%s</a>' %(str(d),str(d))
	return '<td>{0}</td>'.format(str(d))

def add_th(d):
	return '<th>{0}</th>'.format(str(d))

def add_tr(d):
	return '<tr>{0}</tr>'.format(str(d))


'''
	字典列表表格化
'''
# 传入字典，修饰成table表的格式
#dt=[{'id':'zhang','cid':'girl','filesize':23323,'ext':'http://www.baidu.com','operate_num':66},{'id':'zhang','cid':'girl','filesize':23323,'ext':'http://www.baidu.com','operate_num':66}]
def dictlist_tableize(dt_list,head=True):
	if head:
		head="".join(map(lambda x:add_th(x),dt_list[0].keys()))
		head=add_tr(head)

	body=""
	for dt in dt_list:
		for k in dt:
			body+=add_td(dt[k])
		body+=add_tr(body)

	table=head+body

	return add_tb(table)



# 表格渲染
def render_table():
	#db=web.database(dbn='mysql',user='root',pw='root',db='study',host='127.0.0.1')
	#infos=db.select('hot_view_00', where="cid=$cid or filesize=$filesize",vars={'cid':'cid1','filesize':'filesize1'})
	infos=[{'id':'zhang','cid':'girl','filesize':23323,'ext':'http://www.baidu.com','operate_num':66},{'id':'wang','cid':'boy','filesize':6666,'ext':'rmvb','operate_num':23}]

	dtable=dictlist_tableize(infos)
	htmlres=render.dbquery(dtable)

	# 结果保存
	f=open('res/webpy_render.html','w')
	f.write(str(htmlres))  #htmlres._d['__body__'])(只有调试的时候才有)
	time.sleep(2)
	f.close()


# 测试入口
if __name__ == "__main__":
	render_table()

