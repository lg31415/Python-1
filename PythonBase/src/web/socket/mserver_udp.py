#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:socket udp通信-服务器端
    Ref:http://blog.csdn.net/moxiaomomo/article/details/7882534
    State：
    Date:2016/11/6
    Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


import hues
import socket, traceback

def mserver():
    host = '127.0.0.1'  # Bind to all interfaces
    port = 51500

    # Step1: 创建socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Step2: 设置socket选项(可选)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Step3: 绑定到某一个端口
    s.bind((host, port))

    # Step4: 监听该端口上的连接
    while 1:
        try:
            message, address = s.recvfrom(8192)
            hues.info("Got data from ", address)
            hues.success("Data is:",message)
            s.sendto("Data is received succeefully", address)  # 告知客户端，信息已收到
        except (KeyboardInterrupt, SystemExit):
            hues.warn("raise")
            raise
        except:
            hues.warn("traceback")
            traceback.print_exc()

if __name__ == "__main__":
    mserver()

