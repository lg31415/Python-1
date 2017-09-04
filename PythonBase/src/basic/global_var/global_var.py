# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：变量作用域测试
'''
import os
import sys

print u'----------global define-------------'
GVAR1=1
var_global=['hawe','wew','zhangsan']
# 可变的global_define
curfname=os.path.realpath(sys.argv[0])
print "[nowwhere]:", __file__
print "[globals]:",GVAR1,var_global,curfname


def globalf1(var1):
    print(u'this is local fun globalf1:',var1)
print u'this is the global fun:globalf1(5) ',globalf1(5)


def mfun1(varin):
    print "来自参数变量：",varin
    print "来自main变量：",var_main
    print "来自global变量：",var_global

def privatevar():
    __pass="1234556"


if __name__ == "__main__":
    var_main='zhangxiao'
    var_in='var_in'
    mfun1(var_in)
    print u'here we call globalf1(6):',globalf1(6)