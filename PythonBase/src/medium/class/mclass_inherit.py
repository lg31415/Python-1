#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:类继承演示
    Ref:
    State：
    Date:2017/6/29
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    父类
'''
class CBase():
    base_class_var1="基类类变量"
    def __init__(self):
        print '基类构造'
        self.base_inst_var1="基类实例-->公共变量"
        self._base_inst_priv_var1="_基类实例-->_私有变量"
        self.__base_inst_priv_var1="基类实例-->__私有变量"

    def __del__(self):
        print '基类析构'

    def base_pubm_1(self):
        print "基类公共方法1"

    def _base_prim_1(self):
        print "_基类私有方法1"

    def __base_prim_1(self):
        print "__基类私有方法1"

'''
    子类
'''
class CSub(CBase):
    sub_class_var1="子类的类变量"
    def __init__(self):
        print '子类构造'
        print "在子类中显示调用父类的构造函数"
        CBase.__init__(self)
        self.sub_inst_var1="子类实例-->公共变量"
        self._sub_inst_priv_var1="子类实例-->_私有变量"
        self.__sub_inst_priv_var1="子类实例-->__私有变量"

    def __del__(self):
        print '子类析构'
        print "在子类中显示调用父类的析构函数"
        CBase.__del__(self)

    def pubm_1(self):
        print "子类公共方法1"

    def _prim_1(self):
        print "_子类私有方法1"

    def __prim_1(self):
        print "__子类私有方法1"

    # 子类调用基类公共函数
    def subinvokebase(self):
        self.base_pubm_1()
        hues.info("调用基类：")
        print "调用基类类变量:",self.base_class_var1
        print "调用基类实例公共变量：",self.base_inst_var1
        print "_调用基类实例私有变量：",self._base_inst_priv_var1

        hues.info("调用子类:")
        print "调用子类类变量:",self.sub_class_var1
        print "调用子类实例公共变量：",self.sub_inst_var1
        print "_调用子类实例私有变量：",self._sub_inst_priv_var1
        print "__调用子类实例私有变量：",self.__sub_inst_priv_var1



# 测试入口
if __name__ == "__main__":
    cs=CSub()
    cs.subinvokebase()

