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


@app.route('/frontpage')
def frontpage():
	print "this is frontpage"
	return "this is frontpage"


if __name__ == "__main__":
	frontpage()
