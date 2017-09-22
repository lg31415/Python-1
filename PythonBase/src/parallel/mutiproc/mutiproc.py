#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
    功能注释：python多进程
    参考：http://blog.csdn.net/dutsoft/article/details/70336462
'''
import os
import hues
import time
import multiprocessing

'''
import types
import copy_reg
def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)
'''

count=0

# 子进程要执行的代码
f=open('last.log','w')
def child_proc(name):
    global count
    count=count+1
    print 'run child process %s (pid:%s),count:%s' % (name, os.getpid(),str(count))
    print "child process end."
    time.sleep(0.1)
    f.write("subres: "+name+"\n")
    return "subres: "+name


class MutiProcBase(object):
    def __init__(self):
        self.count=1
    '''
        方法1：fork调用
        由于windows不支持fork调用，下面的的mutiproc()在windows上会报错
    '''
    def mmutiproc(self):
        print "now_proc_pid:",os.getpid()
        pid=os.fork()
        if pid==0: # 当前进程已经是子进程
            print 'I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid())
        else:     # 当前进程是父进程，创建了pid的子进程
            print 'I (%s) just created a child process (%s).' % (os.getpid(), pid)

    '''
        方式2：使用封装的mutiprocessing库
    '''
    # 子进程要执行的代码
    def child_proc(self,name):
        print 'run child process %s (%s)...' % (name, os.getpid())
        print "child process end."
        time.sleep(2)
        return "subres: "+name

    # 简单调用
    def base_mutiproc(self):
        hues.info('Parent process start %s.' % os.getpid())
        p = multiprocessing.Process(target=self.child_proc, args=('test',))
        print 'Child Process will start....'
        p.start()
        p.join()
        hues.info("Parent Process end....")

    # 进程池调用（若需要启动大量的子进程时候使用）
    def pool_mutiproc(self):
        hues.info('Parent process start %s.' % os.getpid())
        pool=multiprocessing.Pool(processes=4)
        # 循环开始
        for i in xrange(12):
            msg = "me %d" %(i)
            #pool.apply_async(self.child_proc,args=(msg,))  #有问题，使用内部类的方法有问题，建议所有的子进程都放方法外
            pool.apply_async(child_proc,args=(msg,))
            #pool.apply(child_proc,args=(msg,))
        pool.close()
        pool.join()
        hues.info("Parent Process end....")

    def map_mutiproc(self):
        hues.info('Parent process start %s.' % os.getpid())
        pool=multiprocessing.Pool(processes=4)
        # 循环开始
        pool.map(self.child_proc,['a','b','c','d','e'])
        pool.close()
        pool.join()
        hues.info("Parent Process end....")

# 测试入口
if __name__ == "__main__":
    bmp=MutiProcBase()
    bmp.pool_mutiproc()
    #bmp.map_mutiproc()
    f.close()