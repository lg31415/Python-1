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
	字典表格化
'''
class WebpyTablize(object):
    def __init__(self):
        pass
    def _add_div(self,d):
        return '<div class="table table-condensed">{0}</div>'.format(str(d))

    def _add_tb(self,d):
        return '<table class="table table-hover">{0}</table>'.format(str(d))

    def _add_td(self,d):
        if 'http' in str(d):
            d='<a href="%s">%s</a>' %(str(d),str(d))
        return '<td>{0}</td>'.format(str(d))

    def _add_th(self,d):
        return '<th>{0}</th>'.format(str(d))

    def _add_tr(self,d):
        return '<tr>{0}</tr>'.format(str(d))

    # 字典列表表格化
    # 传入字典，修饰成table表的格式
    # dt=[{'id':'zhang','cid':'girl','filesize':23323,'ext':'http://www.baidu.com'},{'id':'zhang','cid':'girl','filesize':23323,'ext':'http://www.baidu.com'}]
    def dictlist_tablize(self,dt_list,head=True):
        tb_head=''
        if head:
            tb_head="".join(map(lambda x:self._add_th(x),dt_list[0].keys()))
            tb_head=self._add_tr(tb_head)

        tb_body=""
        for dt in dt_list:
            for k in dt:
                tb_body+=self._add_td(dt[k])
            tb_body+=self._add_tr(tb_body)

        table=tb_head+tb_body
        return self._add_tb(table)


    # 表格渲染
    def render_table(self):
        #db=web.database(dbn='mysql',user='root',pw='root',db='study',host='127.0.0.1')
        #infos=db.select('hot_view_00', where="cid=$cid or filesize=$filesize",vars={'cid':'cid1','filesize':'filesize1'})
        infos=[{'id':'zhang','cid':'girl','filesize':23323,'ext':'http://www.baidu.com','operate_num':66},{'id':'wang','cid':'boy','filesize':6666,'ext':'rmvb','operate_num':23}]

        dtable=self.dictlist_tablize(infos) # 注意这里直接传递的是字符串的形式，没有在web.py的模板里进行二次操作
        htmlres=render.webpy_template(dtable)

        # 结果保存
        f=open('res/webpy_res.html','w')
        f.write(str(htmlres))  #htmlres._d['__body__'])(只有调试的时候才有)
        time.sleep(2)
        f.close()


# 测试入口
if __name__ == "__main__":
    wt=WebpyTablize()
    wt.render_table()

