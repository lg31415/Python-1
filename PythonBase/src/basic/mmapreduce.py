# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：map和reduce操作
           map是映射操作，reduce是归纳操作
'''


'''
   map部分:对序列中的每个元素执行相同的操作
'''
def fmap(x):
    return x+'|'

#将一个列表映射到另一个列表
def mmap():
    ol=list('hello')
    mapresult=map(fmap,ol)
    print(ol,mapresult)

    #列表操作
    print map(lambda x,y:(x+y,x-y),[1,2,3],[2,23,4])

    #zip实现
    print map(None,[1,2,3],[4,56,2])

'''
  Reduce部分:递归处理
'''
def freduce(x,y):
    return  x+y

#将一个列表归纳为一个输出#0123456789
def mreduce():
    list=[str(i) for i in range(10)] #列表表达式
    print(list)

    list_pinjie=''.join(list) #1使用拼接函数得到
    print(list_pinjie)

    reduce_r=reduce(freduce,list) #使用reduceduce递归处理得到拼接的结果
    print(reduce_r)



if __name__ == "__main__":
    mmap()
   # mreduce()

