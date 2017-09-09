#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
    功能注释：python多进程
'''
import os
import multiprocessing as winmproc

'''
    由于windows不支持fork调用，下面的的mutiproc()在windows上会报错
'''
def mmutiproc():
    print "now_proc_pid:",os.getpid()
    pid=os.fork()
    if pid==0: # 当前进程已经是子进程
        print 'I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid())
    else:     # 当前进程是父进程，创建了pid的子进程
        print 'I (%s) just created a child process (%s).' % (os.getpid(), pid)


'''
    windows平台上的python多进程处理
'''
# 子进程要执行的代码
def win_child_mutiproc(name):
    print 'Run child process %s (%s)...' % (name, os.getpid())
    print "Child Process end."

# 调用子进程
def win_main_mutiproc():
    print 'Parent process start %s.' % os.getpid()
    p = winmproc.Process(target=win_child_mutiproc, args=('test',))
    print '>>Child Process will start.'
    p.start()
    p.join()
    print "Parent Process end."

#进程池：若需要启动大量的子进程
def mProcpool():
    pass





# 测试入口
if __name__ == "__main__":
    win_main_mutiproc()