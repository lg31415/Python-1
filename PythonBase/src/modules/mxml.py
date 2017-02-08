#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:http://blog.csdn.net/yueguanghaidao/article/details/7265246
	State：
	Date:2016/12/27
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

from xml.etree import ElementTree


def print_node(node):
	'''''打印结点基本信息'''
	print "=============================================="
	print "node.attrib:%s" % node.attrib  # 属性字典
	if node.attrib.has_key("age") > 0 :
		print "node.attrib['age']:%s" % node.attrib['age']
	print "node.tag:%s" % node.tag
	print "node.text:%s" % node.text      # 这个是什么意义


def mxml(text="xxx"):
	'''''读xml文件'''
	# 加载XML文件（2种方法,一是加载指定字符串，二是加载指定文件）
	root = ElementTree.parse(r"../../data/testxml.xml")
	#root = ElementTree.fromstring(text)

	# 获取element的方法
	# 1 通过getiterator
	lst_node = root.getiterator("person")
	for node in lst_node:
		print_node(node)

	# 2通过 getchildren
	lst_node_child = lst_node[0].getchildren()[0]
	print_node(lst_node_child)

	# 3 .find方法
	node_find = root.find('person')
	print_node(node_find)

	#4. findall方法
	node_findall = root.findall("person/name")[1]
	print_node(node_findall)



if __name__ == "__main__":
	mxml()

