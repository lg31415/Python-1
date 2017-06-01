#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:全局变量配置
	Ref:
	State：
	Date:2017/6/1
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


# 显示进度
def process_status(cur,total):
	ratio=round(float(cur)*100/total,2)
	hues.log(str(ratio)+'%')


# 测试入口
if __name__ == "__main__":
    process_status(2,23)

