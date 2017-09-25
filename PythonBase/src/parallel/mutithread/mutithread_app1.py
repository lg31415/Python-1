#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:多线程-生产者消费者模式
    Ref:http://www.toutiao.com/i6466753983980503565/
    State：
    Date:2017/9/21
    Author:tuling56
'''

import hues
import random
import re, os, sys

reload(sys)
sys.setdefaultencoding('utf-8')


import threading
glock=threading.Lock()  # 全局锁


# 全局变量
page_list=['1','2']
item_list=[] # 共用队列

class Producer(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.tid=name
        hues.info("生产者:%s" %self.tid)
    def run(self):
        while len(page_list)>0:
            try:
                glock.acquire()
                page=page_list.pop()
                # do something to item_list using page
                for x in xrange(10):
                    item = random.random()
                    item_list.append(item)
                    print '[producer %s] produce: %s' %(self.tid,item)
            except Exception,e:
                print str(e)
            finally:
                glock.release() # 使用完后要及时释放锁，方便其它线程使用


class Consumer(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.tid=name
        hues.info("消费者:%s" %self.tid)
    def run(self):
        while len(item_list)>0:
            try:
                glock.acquire()
                if item_list:
                    item=item_list.pop()
                    # do something to item_list
                    print '[consumer %s] consumer: %s' %(self.tid,item)
            except Exception,e:
                print str(e)
            finally:
                glock.release()  #保证锁一定会释放



# 测试入口
if __name__ == "__main__":
    # 两个生产者线程
    for x in range(2):
        tid='producer_'+str(x)
        Producer(tid).start()

    # 5个消费者线程，从item_list中取元素进行处理
    for x in range(5):
        tid='consumer_'+str(x)
        Consumer(tid).start()
