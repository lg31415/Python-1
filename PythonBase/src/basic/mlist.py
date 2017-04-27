# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：列表学习
'''

import  re
import pprint

### 全局变量
mylist = ["It's", 'only', 'a', 'model']
mynumlist=range(5)


# 列表基本操作
class LISTBASIC():
    def __init__(self):
        pass
    def list_basic(self):
        dl=mylist*2
        dl+=('nww','xw4r3')
        print dl

    # 列表遍历的四种方法
    def visit_list(self):
        for index, item in enumerate(mylist):
            print(index, item)

        for index in range(len(mylist)):
            print index,mylist[index]

        for item in mylist:
            print item

        for item in iter(mylist):
            print item




# 部分列表操作map
def fmap(x):
    x=x+1
    return  x
def partlistOper():
    global mynumlist
    newlist=map(fmap,mynumlist)
    print newlist
    mynumlist=newlist
    print mynumlist


# 列表计数
from  collections import Counter
from  random import  randrange
def listcount1():
    mycounter1={}
    mycounter=Counter()
    for i in range(100):
        rand_num=randrange(10)
        mycounter[rand_num]+=1
        mycounter1[rand_num]+=1
    for i in range(10):
        print(i,mycounter[i])
        print(i,mycounter1[i])

# 统计list中所有元素和每个元素的个数
from operator import itemgetter
def listcount2():
    l=list('abcddwadekadewdadwerjjnweretraawwer')
    lcount={}
    for i in l:
        try:
            lcount[i]+=1
        except Exception:
            lcount[i]=1
    print  sorted(lcount.iteritems(), key=itemgetter(1), reverse=True)  # 返回排序后的结果

#并行遍历
'''
    zip和map函数：zip将两个列表构建成元组的列表对
    参考：http://blog.sina.com.cn/s/blog_70e50f090101lat2.html
'''
def parallelVisit():
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

    #

#列表排序
def getKey(item):
    img=item.split('.')[0]
    pos=img.split('_')[-1]
    return  img,pos
def list_sort():
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


#列表推导式子 [表达式 for 变量 in 列表 if 条件]
def list_tuidao():
    li=[1,2,3,5,6]
    li_tuidao=[(x,x*10) for x in li]
    print li_tuidao    #[(1, 10), (2, 20), (3, 30), (5, 50), (6, 60)]
    tuidao_dict=dict(li_tuidao)  # {1: 10, 2: 20, 3: 30, 5: 50, 6: 60}
    print tuidao_dict


#动态生长的列表
def listGrow():
    res=((1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16))
    results=[] #空列表
    for index,item in enumerate(res):
        '''
        movieid=item[0]
        title=item[1]
        uv=item[2]
        pv=item[3]
        results.append([movieid,title,uv,pv])
        '''
        results.append(list(item))
        type,title='niw','we'
        results[index].append(type)
        results[index].append(title)
    print 'res:\n',res
    print 'results:\n',results


#列表去重复元素
def listrepr():
    l=list('abcddwadekadewdadwerjjnweretraawwer')
    for x in l:
        while l.count(x)>1:
            l.remove(x)
    l.sort()
    print l

#合并列表的相邻元素
# 参考：http://www.cnblogs.com/Lands-ljk/p/5746837.html
def merge_neighbor():
    a=range(10)
    print type(zip( a[::2], a[1::2]))
    print list(zip( a[::2], a[1::2] ))

# 列表分割
def split_list():
    a=range(10)
    print list(zip( *[iter(a)]*2 ))


if __name__ == "__main__":
    # mlist()
    #listcount()
    #listGrow()
    #dict_sort()
    #list_sort()
    #list_tuidao()
    # parallelVisit()
    #partlistOper()
    #listrepr()
    #print mynumlist
    merge_neighbor()

