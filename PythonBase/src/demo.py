#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:
    Author:tuling56
    Date:
'''
import os,sys
import time
from datetime import date, datetime, timedelta

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')


# 如何引入自定义的包
'''
sys.path.append('E:/Code/Git/Python/tools')
from utily import global_var as gv
from utily import dur_stat as ds
from files import autobackup
import python_invoke_shell as ps
gv.process_status(2,12)
sys.exit()
'''


# 日期参数处理
if len(sys.argv) <= 1:
    yesterday = date.today() - timedelta(days=1)
    yesterday = yesterday.strftime("%Y%m%d")
else:
    yesterday = sys.argv[1]

curdir=os.getcwd()
datapath=curdir.replace("/bin","/data")
logpath=curdir.replace("/bin","/log")

'''
    面向过程
'''
#### 准备工作
def create_dir():
    try:
        if not os.path.exists(datapath):
            os.mkdir(datapath)
        if not os.path.exists(logpath):
            os.mkdir(logpath)
    except Exception,e:
        print str(e)
    

#### func program
def fun_run():
    try:
        a='12345'
        print a[:-1]
        b=[1,2,3,4,5,6,7,'hhahj']
        print b
    except Exception,e:
        s=sys.exc_info()     # 获取系统的执行信息(返回的信息是个元组)
        print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)
    #except Exception,e:
    #   (type, value, traceback) =  sys.exc_info()
    #   print type,value,traceback,e

### 测试函数
def testF():
    print "测试函数"
    fun_run()
    

'''
    面向对象：class object
'''
class CTest(object):
    '''
        classdocs:http://www.jb51.net/article/49402.htm
    '''
    name='hallo '  #类变量
    
    #初始化构造函数 
    def __init__(self,name): 
        #self.name=self.__class__.name  # 实例的成员变量用类变量进行赋值
        self.name=name
        self.age=10
        
    #def __init__(self):
        #print 'defaut constructor no arguments '
  
    def tellyourself(self):           
        print"this is Test class.tellyourself() method"
        print self.name  # 父类的初始化构造函数参数无法传递
        #print(self)     # self代表类的实例
        #print(self.__class__) #self.class指向类
    
    #普通实例方法就是类的实例能都调用的方法   
    def instanceMethod(self):
        print self.name
   
    #静态方法
    @staticmethod
    def staticMethod(): #在定义的时候不传类实例
        print "this is static class method and i am" 
        
    #类方法是将类本身作为对象进行操作的方法，类对象和类实例都可以调用类方法
    @classmethod
    def classMethod(cls,x):
        print cls.name*x #类的成员变量

# 测试类
def testC():
    print "测试类"
    myc=CTest('hahha') ;
    myc.instanceMethod()   #myc.printstr(); #等同于调用Test.printstr(myc)printstr在定义时没有参数，在调用的时候传递了参数
    CTest.classMethod()    #在调用的时候也不传类实例，但提示错误    



# 测试入口
if __name__ == "__main__":
    testF()

