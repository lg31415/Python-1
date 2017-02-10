# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：字典的学习
'''

from  collections import Counter
from  random import  randrange
import pprint

#全局变量
mydict={'zhang':'san','li':'shi','wang':'er'}

#字典基本操作
def mdict():
    if 's1n' in mydict.itervalues():
        print("wrong")
    else:
        print "ringhr"

    locdict={'1':'2','3':'5'}
    #locdict.popitem()
    locdict.update(mydict)
    print locdict.items()

# 字典计数
def mcounter():
    mycounter1={}
    mycounter=Counter()  #用计数器的方式实现
    for i in range(100):
        rand_num=randrange(10)
        mycounter[rand_num]+=1
        mycounter1[rand_num]+=1

    for i in range(10):
        print(i,mycounter[i])
        print(i,mycounter1[i])


##字典元素遍历
def mdictVisit():
    dict = {'Name': 'Zara', 'Age': 7}

    #获取字典中的key的值的两种方法
    print "Value : %d" %  dict.get('Age')
    print "Value : %d" %  dict['Age']

    #如果没有这个键值，则返回指定的“Never Exist”，若不指定，且没有找到则返回None
    print "Value : %s" %  dict.get('Sex',"Never Exist")
    print  dict.has_key('Age')   #1
    print  'Age' in dict.keys()  #2
    print  'Age' in dict         #3  其中1,2,3是等价的
    #print  [dict.keys()]contains 'Age'

    #字典的迭代
    for key,value in dict.iteritems():
        print (key,value)
    for key in dict.keys():
        print(key+":"+str(dict[key]))

    #将字典转化成嵌套列表
    print dict.items()
    for key,value in dict.items():
        print key,value


#字典排序（字典是无序的）
'''
使用dict时，Key是无序的。在对dict做迭代时，我们无法确定Key的顺序。
如果要保持Key的顺序，可以用OrderedDict：
'''
from collections import OrderedDict #排序字典
def dict_sort():
    #method 1 (按value排序)
    mdict={'zhang':1,'wang':2,'yin':8}
    dict_sorted=sorted(mdict.iteritems(),key=lambda asd:asd[1],reverse=False)
    print(mdict,dict_sorted)          #排序后成了元组列表，而不是字典了和原来的格式不一样了

    # method1 (按key排序)
    from operator import itemgetter
    dict_sorted=sorted(mdict.items(),key=itemgetter(0),reverse=True)
    for word, count in dict_sorted:
        print '%s %s'% (word, count)

    #method 2
    cd=dict([('a', 1), ('b', 2), ('c', 3)])   #从列表到字典的构建（无序）
    print cd
    od=OrderedDict([('a', 1), ('c', 2), ('b', 3)]) #从列表到字典（有序）（按原始顺序）
    print  od

    #注意：
    od=OrderedDict()
    od['b']=1
    od['c']=2
    od['a']=3
    print od.keys()

    #字典的构造
    d = dict(name='Bob', age=20, score=88)
    print(d)



#字典推导式
def dict_tuidao():
    my_phrase = ["No", "one", "expects", "the", "Spanish", "Inqution"]
    mydict={key:value for key,value in enumerate(my_phrase)}  #构建字典
    print(mydict)

    #交换字典的键和值
    reversed_dict={value:key for key,value in mydict.items()} #items和iteratoms的区别
    print(reversed_dict)

# 交换字典的键值
# 参考：http://www.cnblogs.com/Lands-ljk/p/5746837.html
def reverse_dict():
    mdict={'zhang':1,'wang':2,'yin':8}
    k=mdict.keys()
    v=mdict.values()
    rmdict=dict(zip(v,k))
    print(rmdict)

#字典设置默认值
from collections import defaultdict
def setDictDefault():
    #method 1
    x={}
    x.setdefault(1,0)
    #x[1]=2
    x[2]=3
    x.setdefault(2,5) #只有初始化的时候才生效，当被赋值过后，其值被更新为新值
    print x

    #method 2
    md=defaultdict(lambda :'N/A')
    md['key1']='23'
    print md['key2']

if __name__ == "__main__":
    #mbase()
    #mdictoper()
    #mdictVisit()
    #dict_sort()
    #setDictDefault()
    reverse_dict()
