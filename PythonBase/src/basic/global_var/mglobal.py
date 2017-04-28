# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：Python测试变量作用域
'''
import globalvars as glv

print u'------------invoke here-----------'

mlocalgvar=2

def run(var):
    #global  GVAR1
    var+=5;
    print var
    print u"本地传递的的变量是",mlocalgvar


print u'>>>>>这里是来自于混合变量的函数'
run(mlocalgvar)

mlocalgvar2=23


if __name__ == "__main__":
    print u'>>>>main函数开始执行'
    mainlocalvar=3
    run(mlocalgvar)
    glv.globalf1(mlocalgvar)
