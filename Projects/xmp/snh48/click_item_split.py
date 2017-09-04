#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,re,os,re
from urllib import quote,unquote
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


if len(sys.argv) <= 1:
    print u"请输入要处理的文件"
    click_data="./snh48_list_type_click_20170417.log"
    #sys.exit()
else:
    click_data = sys.argv[1]

'''
    字符串hex化
    输入：中国
    输出：%E4%B8%AD%E5%9B%BD
'''
def str2hex(instr):
    hexs=instr.encode('hex')
    hexss=[hexs[x:x+2] for x in range(0,len(hexs),2)]
    hexstr='%'+'%'.join(hexss)
    print "hex:",hexstr
    return  hexstr

def mquote(instr):
    hexstr=quote(instr)
    print "hex:",hexstr
    return  hexstr

'''
    字符串反hex化
    输入：%E4%B8%AD%E5%9B%BD
    输出：中国
'''
def hex2str(hexstr):
    hexstr=hexstr.replace('%','')
    print "剔除%:",hexstr
    unhexstr=hexstr.decode('hex')
    print "反hex:",unhexstr
    return unhexstr

def munquote(hexstr):
    unhexstr=unquote(hexstr)
    #print "反hex:",unhexstr
    return unhexstr


'''
    线上测试
'''
# 点击数据分割
def click_item_split():
    with open(click_data,'r') as f:
        for line in f:
            print "src：",line.strip()
            try:
                date,item=line.strip().split('\t')
                litem = item.split('&')
                data_set={"type":"","subtype":"","team":"","group":"","member":"","year":""}
                for itempair in litem:
                    if len(itempair)>0 and itempair.find('=')!=-1:
                        key,value = itempair.split("=")
                        if value.find('%')!=-1:
                            value=munquote(value)
                        if key in data_set :
                            data_set[key] = value
                print "res:","\t".join([date,data_set["type"],data_set["subtype"],data_set["team"],data_set["group"],data_set["member"],data_set["year"]])
            except:
                t,value,traceback = sys.exc_info()
                print t,value
                continue


# 测试入口
if __name__=="__main__":
    '''
    mquote("中国")
    str2hex("中国")
    hex2str(str2hex("中国"))
    munquote(mquote("中国"))
    '''
    click_item_split()