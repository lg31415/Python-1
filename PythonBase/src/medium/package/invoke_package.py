#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:打包和使用包
	Ref:
	State：持续更新
	Date:2017/6/2
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

'''
	包的上一层路径
'''
def minvoke_package_pred_1():
	sys.path.append('E:/Code/Git/Python/tools')  # 加入的包的上一层搜索路径，
	from utily import global_var as gv
	from utily import dur_stat as ds  			 # 导入搜索路径下的包
	from files import autobackup  				 # 如果搜索路径的子文夹不是包的时候就会导入错误
	import python_invoke_shell as ps  			 # 可以导入搜索路径下的子模块


# 不暴露包（init.py文件的使用）
def minvoke_package_pred_2():
	sys.path.append('E:/Code/Git/Python/tools')
	import utily
	from utily.global_fun import ipstr2int
	print ipstr2int('10.65.21.122')


'''
	包的当前路径
'''
# 包的引入方式
def minvoke_package_cur():
	sys.path.append('E:/Code/Git/Python/tools/utily')
	import global_var as gv

	gv.process_status(2, 12)
	sys.exit()


# 测试入口
if __name__ == "__main__":
    minvoke_package_pred_2()
    minvoke_package_cur()

