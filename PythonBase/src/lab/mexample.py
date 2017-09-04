#-*-coding:utf-8-*-

###一些公用的模块文件
import os
import sys


#交互部分,要用python xx.py的方式运行，直接F5会提示错误
def inter():
    name=raw_input("your name?\n")
    print "hello "+name+"!"

#使用python进行绘图
def m_plot():
    import matplotlib.pyplot as plt 
    import numpy as np
    x = np.arange(0, 10, 0.2)
    y = np.sin(x)
    plt.plot(x, y)
    plt.show()

#读取网文件
def readhtml():
    import urllib
    htmlresutl=urllib.urlopen("http://www.baidu.com").read()
    print htmlresutl

#进程和线程
def process_thread():
    #获取path的环境变量
    path=os.environ.get('PATH')
    print path
    #生成一个新的环境变量
    os.environ['cccddd']='ccddd'
    #获取所有的环境变量
    for key in os.environ.keys():
        print key,'\t',os.environ[key]

#数据结构---字典
def m_dict():
    jj={}
    jj['dpg']='2323'
    jj[1]=23
    print jj


#数据结构---列表（集合）
def list_set():
    z=[[1,23,'m43'],[34,'we']]
    f=[23,'rer']
    d=set(z)
    k=set(f)
    print d|k

#数据结构---元组
def m_tuple():
    tuple_name=("apple","banana","grape","orange")
    a,b,c,d=tuple_name   #序列解包
    print a,b,c,d   #逗号分隔不可少
    d,c,b,a=a,b,c,d   #简单的数据交换
    print a,b,c,d   

    #定义只有一个元素的元组,逗号不可少
    test=(0,)
    print type(test)
    pass

###运算符--逻辑运算
def m_opertor():
    print 'a' and 'b' #返回的不是布尔值，而是实际参与进行比较的值之一
    print '' and 'b'


###流程控制
def flow_control():
    #if elif else
    x='4'
    print 'ok'
    if x=='1':
        print 'one'
    elif x=='2':
        print 'two'
    else:
        print 'nothing'
    numtrans={1:'one',2:'two',3:'three'}
    try:
        print numtrans[x]
    except KeyError:
        print 'nothing'
    else:
        pass
    finally:
        pass
    
#列表表达式
def list_express():
    x,y,m,n=1,2,3,4  #序列赋值
    #x=1,y=2,m=3,n=4  #这样是错误的
    sum=lambda x,y:x+y
    print sum #显示的是函数地址（Lambda表达式的地址）
    sub=lambda m,n:m-n
    print sub
    return sum(x,y)*sub(m,n)

#函数
'''
    Python支持完全的面向对象编程，同时也支持过程式编程,对参数类型的不要求，
    也使得其支持泛型编程,函数的嵌套定义：
    （1）内存函数可以访问外层函数中定义的变量，但不能重新赋值
    （2）内存函数的local namespace 不包含外层函数定义的变量，除非手动引入
'''
def m_fun():
    i=0
    def F1():
        print "this is f1(),i "+str(i)+" first come index"
    def F2(x,y):
        F1()
        a=x+y
        print locals()
        i=1;  #在F2()中试图修改外层函数的变量，表面上修改成功，但是在F3()函数中可以看到结果并未修改
        print i
    def F3():
        print i
    #print globals()
    #F1()
    F2(3,4)
    F3()

#函数返回多个值    
def operator(x=1,y=2,operator='+'):
    result={  #字典
    "+":x+y,
    "-":x-y,
    "*":x*y,
    "/":x/y
    }
    return  x,y,operator,result.get(operator) #字典的get方法

##类
'''
    常规方法的默认第一个参数都是self,私有成员变量的定义以“__”开始，直接定义在类中的是静态成员变量
    定义在初始化函数中的是公有成员变量
'''
class Person(object):
    def __init__(self, name,age):
        super(Person, self).__init__()
        self.name = name
        self.__age=age
        print "Person init....."
    def getName(self):
        print "Name is %s"%self.name
    def getAge(self):
        print "Age is %s"%self.__age

class Student(Person):
    stdid=2                      #定义静态成员变量
    def __init__(self,name,age): #初始化构造函数
        self.name=name           #定义公共成员变量
        self.__age=age           #定义私有成员变量
        print 'Student init....'
    def getNameAge(self): 
        format="my name is %s , my age is %d"%(self.name,self.__age)
        print format

    def getInfo(self):            #不能定义一个不操作实例的方法！！！,若该方法不操作实例，则其调用的方法必须操作实例
        Student.getNameAge(self)

    @staticmethod                 #静态方法的定义
    def getInfo():
        print "this is static method"

    def __del__(self):           #析构函数
        print 'Student delete...'



        

####这是主程序####
if __name__ == '__main__':
    #readhtml()
    #m_tuple()
    #m_opertor()
    #flow_control()
    #print list_express()
    
    ####函数
    #函数定义
    #m_fun()
    #函数多返回值
    #x,y,operator,result=operator(1,2,'-')
    #print str(x)+operator+str(y)+'='+str(result)
    
    ####类的使用
    #方法的调用
    student=Student("chu",32)
    student.getInfo()  #通过实例调用的方法，为什么也是静态方法，重载的那个与实例相关的方法怎么调用???
    Student.getInfo()
    
    #变量的使用
    #print student.name   #打印公共成员变量
    #print Student.stdid  #打印静态成员变量,不初始化就可以直接访问
    #print student.__age  #打印私有成员变量出错！！！
    #类的继承
    
    
