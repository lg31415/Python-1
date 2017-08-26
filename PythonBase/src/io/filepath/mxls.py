#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:Python修改并保存当前excel文件
	Ref:http://www.toutiao.com/i6344931811272950273/
	    http://www.python-excel.org/
	State：未完成测试
	Date:2017/8/26
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import xlrd
import shutil
from xlutils.copy import copy
from xlutils.margins import null_cell_types

class Cmxls():
    def __init__(self):
        self.outxls='out.xlws'

    def mxls(self):
        r_xls=xlrd.open_workbook(self.outxls)
        table = r_xls.sheet_by_index(0)
        nrows=table.nrows
        ncols = table.ncols

        #write the column key
        w_xls = copy(r_xls)
        sheet_write = w_xls.get_sheet(0)
        sheet_write.write(0, 1, "Bug ID")
        sheet_write.write(0, 2, "New Bug")
        sheet_write.write(0, 3, "Comments")
        sheet_write.write(0, 4, "Bug Close")
        w_xls.save(self.outxls)

# 测试入口
if __name__ == "__main__":
    cxls=Cmxls()
    cxls.mxls()

