#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun: scoket udp通信-客户端
    Ref:http://blog.csdn.net/moxiaomomo/article/details/7882534
    State：send和receive的参数字节问题。避免接收不全的情况
    Date:2016/11/6
    Author:tuling56
'''
import os
import sys
import re
import time

reload(sys)
sys.setdefaultencoding('utf-8')

import hues
import socket, sys

def mclient():
    # Step1: 输入host和port信息
    host ='127.0.0.1'   #raw_input('please input host name: ')
    port ='51500'        #raw_input('please input textport: ')

    # Step2: 创建socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        port = int(port)
    except ValueError:
        port = socket.getservbyname(port, 'udp')

    # Step3: 打开socket连接
    s.connect((host, port))  # 不管是tcp还是udp的都有connnect方法


    hues.log("Looking for replies; press Ctrl-C or Ctrl-Break to stop")
    while 1:
        # Step4: 发送数据
        hues.log("Enter data to transmit: ")
        data = sys.stdin.readline().strip()
        s.sendall(data)
        #s.sendto(data)

        # Step5: 接收服务器发过来的数据(一直在等待服务器发送过来的数据)
        buf = s.recv(2048)
        if not len(buf):

            break
        #sys.stdout.write(buf)
        hues.success(buf)
        time.sleep(5)
    s.close()

if __name__ == "__main__":
    mclient()

