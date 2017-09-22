#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:进程通信
    Ref:https://segmentfault.com/a/1190000008122273
    State：
    Date:2017/8/29
    Author:tuling56
'''
import re, os, sys
import hues
import random

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    进程通信:Pipe实现
'''
from multiprocessing import Pipe, Process
class MutiProcTalkByPipe(object):
    def __init__(self):
        pass

    def _son_process(self,x, pipe):
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

    def proc_talk_pipe(self):
        out_pipe, in_pipe = Pipe(True)
        son_p = Process(target=self._son_process, args=(100, (out_pipe, in_pipe)))
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
'''
from multiprocessing import Queue, Process
from Queue import Empty as QueueEmpty
class MutiProcTalkByQueue(object):
    def __init__(self):
        pass

    def _getter(self,name, queue):
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

    def _putter(self,name, queue):
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

    def proc_talk_queue(self):
        queue = Queue()
        getter_process = Process(target=self._getter, args=("Getter", queue))
        putter_process = Process(target=self._putter, args=("Putter", queue))
        getter_process.start()
        putter_process.start()



# 测试入口
if __name__ == "__main__":
    mbtp=MutiProcTalkByPipe()
    mbtp.proc_talk_pipe()

    mbtq=MutiProcTalkByQueue()
    mbtq.proc_talk_queue()

