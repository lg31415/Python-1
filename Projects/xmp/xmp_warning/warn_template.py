#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:
	State：
	Date:2017/8/30
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


def fun():
    items={'jingpin_pv':"次数","jingpin_uv":"人数"}
    header=["日期(上周同期)"]
    header.extend(map(lambda key:key+"\t上周同期"+key,items.values()))
    header='\t'.join(header)
    body_list=['a.date','b.date']
    for item in items.keys():
        statitem="a.%s,b.%s,concat(round((a.%s-b.%s)*100/b.%s,2),'%%')" %(item,item,item,item,item)
        body_list.append(statitem)
    body=','.join(body_list)

    print header
    print body

# 测试入口
if __name__ == "__main__":
    fun()

