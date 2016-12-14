#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：Python脚本中执行其它非Python程序
'''
import os
import subprocess

def run():
    res=subprocess.call(('dir','D:\\'),shell=True)
    #print type(res),res

    res=subprocess.Popen()


if __name__ == "__main__":
    run()
