#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:超时处理
    Ref:https://stackoverflow.com/questions/3471461/raw-input-and-timeout
    State：利用多线程的跨平台解决方案未完成，问题出在不能退出环节
    Date:2017/9/5
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


# linux平台上
def linux_platform():
    from select import select

    timeout = 10
    print "Enter something:",
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        s = sys.stdin.readline()
        print s
    else:
        print "No input. Moving on..."

# windows平台
def windows_platform(caption, default, timeout = 5):
    import time,msvcrt
    start_time = time.time()
    sys.stdout.write('%s(%s):'%(caption, default))
    input = ''
    while True:
        if msvcrt.kbhit():
            chr = msvcrt.getche()
            if ord(chr) == 13: # enter_key
                break
            elif ord(chr) >= 32: #space_char
                input += chr
        if len(input) == 0 and (time.time() - start_time) > timeout:
            break

    print ''  # needed to move to next line
    if len(input) > 0:
        return input
    else:
        return default

# 跨平台解决方案（未完成）
input_v=''
import threading,time
def all_platform(caption,default,timeout=5):
    def t_input():
        global input_v
        hues.success("current thread %s is running" %(threading.current_thread().name))
        input_v=raw_input("Please type a name(john):")
        hues.success("current thread %s is end,value is %s" %(threading.current_thread().name,input_v)) #这个始终没有退出

    #start_time=time.time()
    #sys.stdout.write('%s(%s):'%(caption, default))
    try:
        t=threading.Thread(target=t_input,name="sub_input")
        t.start()
        t.join(timeout=timeout)
        #print "线程外input_v的值是:",input_v
        if len(input_v)>0: #and (time.time()-start_time)>timeout:
            return input_v
        else:
            return default
    except Exception,e:
        print str(e)


# 测试入口
if __name__ == "__main__":
    # linux平台
    #lins=linux_platform()

    # windows平台上
    #wins = windows_platform('Please type a name', 'john')
    #print 'The name is %s' % wins

    # 跨平台
    hues.success("current thread %s is running" %(threading.current_thread().name))
    ans=all_platform('Please type a name', 'john')
    print 'The name is %s' % ans
    hues.success("current thread %s end" %(threading.current_thread().name))
    sys.exit()
