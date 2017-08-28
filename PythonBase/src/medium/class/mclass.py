#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    功能：类演示
    Created on 2015年8月10日
    @author: yjm
    Ref:http://python.jobbole.com/82297/
        http://www.jb51.net/article/49402.htm
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import hues


'''
    基类
'''
gloabvar1="zhang+xiang+wang"
class Test(object):
    '''
        类描述
        source:http://www.jb51.net/article/49402.htm
    '''
    name='hallo '  # 类变量
    def __init__(self,name): # 构造函数
        hues.info("调用基类的构造函数，需要传递name参数")
        #self.name=self.__class__.name  # 实例的成员变量用类变量进行赋值
        self.name=name # 实例的成员变量在初始的时候由类的构造函数传递过来

    def __del__(self):
        hues.info('调用基类的析构函数，defaut constructor no arguments ')

    def tellyourself(self):
        print "this is Test class.tellyourself() method"
        print self.name  # 父类的初始化构造函数参数无法传递
        # print(self) # self代表类的实例
        # print(self.__class__) # self.class指向类

    # 实例方法就是类的实例能都调用的方法
    def instanceMethod(self,para1):
        print self.name
        print '实例方法接收的参数:',para1
        print '实例方法调用另一个方法'
        self.tellyourself()
        self.staticMethod()

    # 静态方法
    @staticmethod
    def staticMethod(): # 在定义的时候不传类实例
        print "this is static class method and i am"

    # 类方法：是将类本身作为对象进行操作的方法，类对象和类实例都可以调用类方法
    @classmethod
    def classMethod(cls,x):
        print cls.name*x # 类的成员变量

'''
	继承类
'''
class subTest(Test):
    '''
        subTest类继承自Test父类
    '''
    def __init__(self,name):
        self.name="我是子类的构造函数传递过来的name"
        hues.info("调用子类的构造函数")
        hues.info("子类调用父类的构造函数")
        #Test.__init__(self,name) # 显示调用父类的构造函数

    def __del__(self):
        hues.info("调用子类的析构函数")

    def tellyourself(self):
        print '子类调用父类的方法', self.name
        super(subTest,self).tellyourself() # 父类没有机进行初始化构造啊

    def testyourself_son(self):
        hues.info("子类调用自身的方法")



# 测试入口
if __name__=="__main__":
    '''
        基础类
    '''
    # 实例方法
    myc=Test('类学习')
    myc.instanceMethod('this is para1')# myc.printstr(); # 等同于调用Test.printstr(myc)printstr在定义时没有参数，在调用的时候传递了参数
    # Test.classMethod() # 在调用的时候也不传类实例，但提示错误

    # 静态方法
    myc.staticMethod()
    Test.staticMethod()

    # 类方法
    myc.classMethod(3)
    Test.classMethod(2)

    '''
        类的继承
    '''
    # 类的继承和调用
    sc=subTest('I come from sub class') # 子类调用父类的构造函数
    sc.tellyourself()                   # 子类执行父类的实例方法



    # 类变量和实例变量








