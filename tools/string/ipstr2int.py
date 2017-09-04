#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Date:
    Author:tuling56
    Fun: ip字符串和整型进行相互转换
'''
import os
import sys

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

import socket,struct
def ipstr2unit(str):
    return socket.ntohl(struct.unpack("I",socket.inet_aton(str))[0])

def ipstr2int(str):
    uint = socket.ntohl(struct.unpack("I",socket.inet_aton(str))[0])
    return struct.unpack("i", struct.pack('I', uint))[0]

def ipstr2long(ip_str):
    ret = ip_str.split(".")
    num = 0
    for i in range(0,len(ret)):
        num*=256
        num += int(ret[i])
    #return num

    num_new=0
    for i in ret:
        num_new*=256
        num_new+=int(i)
    print num_new

    return num

def ipstr2unitReverse(str):
    return socket.htonl(ipstr2unit(str))

def ipstr2intReverse(str):
    return socket.htonl(ipstr2int(str))

def ipnum2str(ip):
    if ip<0:
        ip = struct.unpack("I", struct.pack('i', ip))[0]
    return socket.inet_ntoa(struct.pack('I',socket.htonl(ip)))
    

if __name__ == "__main__":
    print ipstr2unit("232.23.2.1")
    #print ipstr2int("232.23.2.1")
    #print ipstr2unitReverse("232.23.2.1")
    #print ipstr2intReverse("232.23.2.1")
    #print ipnum2str(ipstr2unit("232.23.2.1"))
    print ipstr2long("232.23.2.1")






