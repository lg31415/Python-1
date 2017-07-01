# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：列表学习
'''

import  re
import pprint

# 全局变量
mylist = ["It's", 'only', 'a', 'model']

'''
    列表基本操作
'''
class CList(object):
    def __init__(self):
        pass

    def basic(self):
        global mylist
        dl=mylist*2
        dl+=('nww','xw4r3')
        print dl

    # 基础遍历
    def visit(self):
        for index, item in enumerate(mylist):
            print(index, item)

        for index in range(len(mylist)):
            print index,mylist[index]

        for item in mylist:
            print item

        for item in iter(mylist):
            print item

    #并行遍历
    '''
        zip和map函数：zip将两个列表构建成元组的列表对
        参考：http://blog.sina.com.cn/s/blog_70e50f090101lat2.html
    '''
    def parallel_visit(self):
        L1=[1,2,3,4]
        L2=[5,6,7,8]
        if len(L1)!=len(L2):
            return
        #print zip(L1,L2),type(zip(L1,L2))
        #print list(zip(L1,L2))
        for (x,y) in zip(L1,L2): # 也可以写成for x,y in zip(L1,L2)
            print x,'+',y,'=',x+y
        #zip和dict结合快速构造字典的方法
        Ld=dict(zip(L1,L2))
        print(Ld)

    # 部分列表操作map
    def fmap(self,x):
        x=x+1
        return  x
    def partoper(self):
        newlist=map(self.fmap,range(5))
        print newlist
        mynumlist=newlist
        print mynumlist

    #列表去重复元素
    def uniq(self):
        l=list('abcddwadekadewdadwerjjnweretraawwer')
        for x in l:
            while l.count(x)>1:
                l.remove(x)
        l.sort()
        print l

    # 列表分割
    def split(self):
        a=range(10)
        print list(zip( *[iter(a)]*2 ))

    #列表推导式子 [表达式 for 变量 in 列表 if 条件]
    def tuidao(self):
        li=[1,2,3,5,6]
        li_tuidao=[(x,x*10) for x in li]
        print li_tuidao    #[(1, 10), (2, 20), (3, 30), (5, 50), (6, 60)]
        tuidao_dict=dict(li_tuidao)  # {1: 10, 2: 20, 3: 30, 5: 50, 6: 60}
        print tuidao_dict

    # 合并列表的相邻元素
    # 参考：http://www.cnblogs.com/Lands-ljk/p/5746837.html
    def merge_neighbor(self):
        a=range(10)
        print type(zip( a[::2], a[1::2]))
        print list(zip( a[::2], a[1::2] ))


from collections import Counter
from random import randrange
from operator import itemgetter
'''
    列表计数、排序、比较
'''
class CListMedium(CList):
    def __init__(self):
        self.list1=list('abcddwadekadewdadwerjjnweretraawwer')
        self.list2=[(1,'zhang'),(2,'wang'),(0.5,'li'),(8,'yin')]

    # 统计list中所有元素和每个元素的个数
    def itemcount1(self):
        mycounter1={}
        mycounter=Counter()
        for i in range(100):
            rand_num=randrange(10)
            mycounter[rand_num]+=1
            mycounter1[rand_num]+=1
        for i in range(10):
            print(i,mycounter[i])
            print(i,mycounter1[i])

    def itemcount2(self):
        lcount={}
        for i in self.list1:
            try:
                lcount[i]+=1
            except Exception:
                lcount[i]=1
        print sorted(lcount.iteritems(), key=itemgetter(1), reverse=True)  # 返回排序后的结果


    #列表排序
    def __getKey(self,item):
        img=item.split('.')[0]
        pos=img.split('_')[-1]
        return img,pos

    def sort(self):
        print('-------列表排序-----')
        '''
        list=[(1,'zhang'),(2,'wang'),(0.5,'li'),(8,'yin')]
        list.sort()
        list.reverse()
        print list #按列表中的第一个元素进行排序

        list_non=[('zhang',1),('wang',2),('li',0.5),('yin',8)]
        list_non.sort()
        list_non.reverse()
        print list_non
        '''
        # 复杂操作（先按列表元素的第一切割排序，再按列表元素的第二切割排序）
        list=['img073.xuanzeti_answer_1', 'img073.xuanzeti_answer_0', 'img073.xuanzeti_answer_8', 'img073.xuanzeti_answer_11', 'img073.xuanzeti_answer_5', 'img073.xuanzeti_answer_9', 'img073.xuanzeti_answer_10', 'img073.xuanzeti_answer_3', 'img073.xuanzeti_answer_7', 'img073.xuanzeti_answer_4', 'img073.xuanzeti_answer_6', 'img073.xuanzeti_answer_2', 'img072.xuanzeti_answer_1', 'img072.xuanzeti_answer_0', 'img072.xuanzeti_answer_8', 'img072.xuanzeti_answer_11', 'img072.xuanzeti_answer_5', 'img072.xuanzeti_answer_9', 'img072.xuanzeti_answer_10', 'img072.xuanzeti_answer_3', 'img072.xuanzeti_answer_7', 'img072.xuanzeti_answer_4', 'img072.xuanzeti_answer_6', 'img072.xuanzeti_answer_2']

        pattern=re.compile(r'[._]')
        llist=map(lambda x:re.split(pattern,x),list)
        llist=map(lambda x:[x[0],x[1],x[2],int(x[3])],llist)
        llist=sorted(llist, key=itemgetter(0,3))
        llist=map(lambda x:x[0]+"."+x[1]+"_"+x[2]+"_"+str(x[3]),llist)
        print(llist)

    # 动态生长的列表
    def grow(self):
        res=((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16))
        results=[] #空列表
        for index,item in enumerate(res):
            results.append(list(item))
            type,title='niw','we'
            results[index].append(type)
            results[index].append(title)
        print 'res:\n',res
        print 'results:\n',results

    # 列表比较
    def cmp(self,l1=[],l2=[]):
        if not l1 or not l2:
            l1=list('abcdabcd')
            l2=list('dcbadcba')
        print l1,l2
        cmpres=cmp(l1,l2)
        print cmpres
        if not cmpres:
            print "l1==l2"
            return True
        else:
            print "l1!=l2"
            return False

#  测试入口
if __name__ == "__main__":
    mlmedium=CListMedium()
    mlmedium.cmp()

