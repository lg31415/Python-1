#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:Python调用shell
    Ref:
    State：还需要完善
    Date:2017/4/12
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

'''
    基础版
'''
import subprocess,shlex
def python_invoke_shell():
    cmd="md5sum python_shell.py"
    p=subprocess(shlex.split(cmd),stdout=subprocess.PIPE)
    print(p.stdout.read())


'''
    增强版
'''
import time
import datetime
def execute_command(cmdstring, cwd=None, timeout=None, isshell=False):
    """执行一个SHELL命令
           封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
           参数:
            cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
            timeout: 超时时间，秒，支持小数，精度0.1秒
            shell: 是否通过shell运行(这个参数的意义是什么？？？？)
    Returns: return_code
    Raises:  Exception: 执行超时
    """
    if isshell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    #没有指定标准输出和错误输出的管道，因此会打印到屏幕上；
    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE,shell=isshell,bufsize=4096)

    #超时检查:subprocess.poll()方法：检查子进程是否结束了，如果结束了，设定并返回码，放在subprocess.returncode变量中
    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s"%cmdstring)

    return str(sub.returncode)

'''
    python调用其它程序
'''
import webbrowser
def python_invoke():
    timeleft=4
    while timeleft>0:
        print(timeleft)
        time.sleep(1)
        timeleft=timeleft-1

    #subprocess.Popen(['start','README.md'],shell=True)
    webbrowser.open('http://www.baidu.com',new=1)

# 测试入口
if __name__ == "__main__":
    #python_invoke_shell()
    #print execute_command("ls")
    python_invoke()
