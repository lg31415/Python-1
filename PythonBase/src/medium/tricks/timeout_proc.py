#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:超时处理
	Ref:https://stackoverflow.com/questions/3471461/raw-input-and-timeout
	State：利用多线程的跨平台解决方案未完成
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
def all_platform(caption,default,timeout=5):
    import time
    start_time=time.time()
    sys.stdout.write('%s(%s):'%(caption, default))
    while True:
        input=raw_input("请输入数据:")  #程序完全卡死在这个地方，需要使用进程通信的方式，，，，
        if len(input)==0 and (time.time()-start_time)>timeout:
            break



# 测试入口
if __name__ == "__main__":
    # linux平台
    #lins=linux_platform()

    # windows平台上
    wins = windows_platform('Please type a name', 'john')
    print 'The name is %s' % wins

    # 跨平台
    ans=all_platform('Please type a name', 'john')
    print ans

