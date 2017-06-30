#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：集合操作
  参考：http://www.jb51.net/article/55561.htm
  状态: 完善中
'''


class CSet():
    setA={'a','cd',1,'wehjer'}
    setB={'a',2,'ef','cd'}

    def __init__(self):
        pass

    def create(self):
        setC=set()       # 创建空集合
        setL=set('abcd') #创建集合｛ａ，ｂ，ｃ，ｄ｝

        setTuidao={x*3 for x in 'abcdef'} #集合解析（集合推导式）
        print(type(setTuidao),setTuidao)

    def addremove(self):
        setAB=self.setA | self.setB
        print('setAB:',setAB)

        setAD=self.setA.add('D') # 错误，集合setAD仍然是空值，只是在集合A中添加了元素'D'
        print('setAD:',setAD)
        print self.setA

        self.setA.remove('D')   # 若要删除的元素不在集合中，则报错
        print self.setA

        self.setA.discard('D')  # 若要删除的元素不在集合中，则什么都不做
        print self.setA

        pope=self.setA.pop()   # 从集合中任意删除一个元素并返回该元素
        print self.setA

        self.setA.update('zhang')
        print self.setA

    def visit(self):
        for el in list(self.setA): # 集合本身不支持遍历操作，只能使用自带的方法来修改
            print el


# 测试入口
if __name__ == "__main__":
    mset=CSet()
    #mset.create()
    mset.visit()
