#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:python装饰器学习
	Ref:http://mp.weixin.qq.com/s/Ru_TpOnelMXPzH-1o34oZw
	State：
	Date:2017/5/17
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


# 定义普通函数
def print_text(name):
	return 'hello,'+name

# 定义的嵌套函数（也就是装饰器）
def add_td(func):
	def prt_func(name):
		return '<td>{0}</td>'.format(func(name))
	return prt_func  # 返回的普通的函数

## 方法一：
# 用add_tb修饰定义的普通函数（返回的是经过装饰后的print_text函数）
hto=add_td(print_text)

print print_text('修饰后')
print hto('修饰后')

## 方法2：
@add_td
def print_name(name):
	return 'hello,my name is '+name

print print_name('NqqFZIow')




if __name__ == "__main__":
	print '装饰器学习'

