#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'yjm'
'''
  功能注释：全局转换库
'''

import os
import sys,re,binascii

##################### preprocess ##########################
def strF2J(ustring):
    '''
    unicode
    '''
    return conv.convert(ustring)
def strQ2B(ustring):
    '''
    unicode
    '''
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:
            rstring += uchar
        else:
            rstring += unichr(inside_code)
    return rstring
def strB2Q(ustring):
    '''
    unicode
    '''
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:
            rstring += uchar
            continue
        if inside_code == 0x0020:
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        rstring += unichr(inside_code)
    return rstring
def simplePreprocess(ustring):
    '''
    unicode
    '''
    #lower
    ustring  = ustring.lower()
    #Q2B
    ustring = strQ2B(ustring)
    #F2J
    try:
        ustring = strF2J(ustring)
    except:
        ustring = ustring
    return ustring

####################### ip ###############################
import socket,struct
def ipstr2unit(str):
    return socket.ntohl(struct.unpack("I",socket.inet_aton(str))[0])
def ipstr2int(str):
    uint = socket.ntohl(struct.unpack("I",socket.inet_aton(str))[0])
    return struct.unpack("i", struct.pack('I', uint))[0]
def ipstr2unitReverse(str):
    return socket.htonl(ipstr2unit(str))
def ipstr2intReverse(str):
    return socket.htonl(ipstr2int(str))
def ipnum2str(ip):
    if ip<0:
        ip = struct.unpack("I", struct.pack('i', ip))[0]
    return socket.inet_ntoa(struct.pack('I',socket.htonl(ip))) 


###################### hex unhex ########################
def hexunhex(s):
    tohex=s
    rest=tohex.encode('hex')
    t=[rest[x:x+2] for x in range(0,len(rest),2)]
    shex='%'+'%'.join(t)
    mres=re.sub(r'%','',shex,0)
    unhex=mres.decode('hex')
    print "Origin:",tohex,"\nHex:",rest,"\nHex%:",shex,"\nUnhex:",unhex

# 输入如    #s="%E9%9A%8B%E5%94%90%E8%8B%B1%E9%9B%84%E4%BC%A0"
def unhex(s):
    mres=re.sub(r'%','',s,0)
    unhex=mres.decode('hex')
    print unhex
    return  unhex

# 去除url中的%符号
def uri2hex(s):
    ret = ""
    length = len(s)
    i = 0
    while i < length:
        if s[i] == '%' and i+2 < length and isxdigit(s[i+1:i+2]):
            ret += s[i+1:i+3]
            i += 3
        else:
            ret += binascii.hexlify(s[i])
            i += 1
    return ret

def uri2hex2(s):
    if not s:
        s='%e4%b8%ad%e6%96%87'
    print uri2hex(s) #e4b8ade69687

    #uri中的%符号用\x进行替换
    print s.replace('%','\\x').decode('utf-8')
    #print u'中文'.encode('utf-8').decode('utf-8')


#######################主测试入口
if __name__ == "__main__":
    #hex unhex
    tohex='隋唐英雄传'
    s="%E9%9A%8B%E5%94%90%E8%8B%B1%E9%9B%84%E4%BC%A0"
    unhex(s)
    #hexunhex(tohex)




