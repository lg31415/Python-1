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
    if pid==0: #当前进程已经是子进程
        print 'I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid())
    else:     #当前进程是父进程，创建了pid的子进程
        print 'I (%s) just created a child process (%s).' % (os.getpid(), pid)


'''
    windows平台上的python多进程处理
'''
# 子进程要执行的代码
def win_child_mutiproc(name):
    print 'Run child process %s (%s)...' % (name, os.getpid())

# 调用子进程
def win_main_mutiproc():
    print 'Parent process %s.' % os.getpid()
    p = winmproc.Process(target=win_child_mutiproc, args=('test',))
    print '>>Child Process will start.'
    p.start()
    p.join()
    print ">>Child Process end."

#进程池：若需要启动大量的子进程
def mProcpool():
    pass
    

'''
    进程通信:Pipe实现
    Ref:https://segmentfault.com/a/1190000008122273
'''
from multiprocessing import Pipe, Process

def son_process(x, pipe):
    _out_pipe, _in_pipe = pipe
    print u"子进程被创建"

    # 关闭fork过来的输入端
    _in_pipe.close()
    while True:
        try:
            msg = _out_pipe.recv()
            print msg
        except EOFError:
            # 当out_pipe接受不到输出的时候且输入被关闭的时候，会抛出EORFError，可以捕获并且退出子进程
            print u"子进程退出"
            break

def proc_talk_pipe():
    out_pipe, in_pipe = Pipe(True)
    son_p = Process(target=son_process, args=(100, (out_pipe, in_pipe)))
    son_p.start()

    # 等pipe被fork 后，关闭主进程的输出端
    # 这样，创建的Pipe一端连接着主进程的输入，一端连接着子进程的输出口
    out_pipe.close()
    for x in range(50):
        in_pipe.send(x)
    in_pipe.close()
    son_p.join()
    print u"主进程也结束了"


'''
    进程通信：Queue实现
    Ref:https://segmentfault.com/a/1190000008122273
'''
from multiprocessing import Queue, Process
from Queue import Empty as QueueEmpty
import random

def getter(name, queue):
    print 'Son process %s' % name
    while True:
        try:
            value = queue.get(True, 10)
            # block为True,就是如果队列中无数据了。
            #   |—————— 若timeout默认是None，那么会一直等待下去。
            #   |—————— 若timeout设置了时间，那么会等待timeout秒后才会抛出Queue.Empty异常
            # block 为False，如果队列中无数据，就抛出Queue.Empty异常
            print "Process getter get: %f" % value
        except QueueEmpty:
            break

def putter(name, queue):
    print "Son process %s" % name
    for i in range(0, 10):
        value = random.random()
        queue.put(value)
        # 放入数据 put(obj[, block[, timeout]])
        # 若block为True，如队列是满的：
        #  |—————— 若timeout是默认None，那么就会一直等下去
        #  |—————— 若timeout设置了等待时间，那么会等待timeout秒后，如果还是满的，那么就抛出Queue.Full.
        # 若block是False，如果队列满了，直接抛出Queue.Full
        print "Process putter put: %f" % value

def proc_talk_queue():
    queue = Queue()
    getter_process = Process(target=getter, args=("Getter", queue))
    putter_process = Process(target=putter, args=("Putter", queue))
    getter_process.start()
    putter_process.start()



'''
    #############主入口#############
'''
if __name__ == "__main__":
    #win_main_mutiproc()
    #proc_talk_pipe()
    proc_talk_queue()
