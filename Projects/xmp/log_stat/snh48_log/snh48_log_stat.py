#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
'''
    Fun:SNH48日志数据统计
    Ref:
    State：进行中，如何将日志分割部分泛化，是一个需要好好想的问题
    Date:2016/12/21
    Author:tuling56
'''
import os, sys
import re
from datetime import date, datetime, timedelta
import json
from collections import defaultdict
import MySQLdb
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) <= 1:
    calcday = date.today() - timedelta(days=1)
    calcday = calcday.strftime("%Y%m%d")
else:
    calcday = sys.argv[1]


file_path=os.getcwd()

log='snh48_log.log'
proc_log='proc_log.log'
stat_res='stat_log.log'

'''
    Part1:构造全备字典部分
'''
# 构造全备类型字典
category_fields=defaultdict(set)
def build_category_fields(log):
    with open(log,"r") as f:
        for line in f:
            try:
                line=line.split('\"')
                category,info=line[1].split('?')
                category = category.split()[1].replace('/', '')

                # 解析请求体(汇总key)
                if not info:continue
                infolist=info.split("&")
                for i in range(0,len(infolist)):
                    if(len(infolist[i])>0) and infolist[i].find('=')!=-1:
                        key,value=infolist[i].split("=")
                        category_fields[category].add(key)
            except Exception as e:
                raise e
            finally:
                pass

# 全备字典也可以手工指定
def handset_category_fields():
    category_fields['category1']={'key1','key2','key3','key4'} 
    category_fields['category1']={'key1','key2','key3','key4'} 
    category_fields['category1']={'key1','key2','key3','key4'} 
    category_fields['category1']={'key1','key2','key3','key4'} 
    
'''
    Part2:文件句柄部分
'''
# 打开文件句柄列表
category_handles={}
def open_category_handles():
    open_handle_num=0
    for category in category_fields.keys():
        try:
            fhandle=open(category+'.data','w')
            titles=','.join([str(ckey) for ckey in category_fields[category]])
            fhandle.write(titles+'\n')
            category_handles[category]=fhandle
            open_handle_num+=1
        except Exception as e:
            print "open %s handle fail" %(category)
            raise e
    return open_handle_num 

# 关闭文件句柄列表
def close_category_handles():
    for category,chandle in category_handles.iteritems():
        try:
            chandle.close()
        except Exception,e:
            print "close %s handle fail" %(category)


'''
    Part3: 1.请求体分割:
    请求体格式："GET /info?groupID=7A01D299C797C_1560846460&type=local&key=7A03E41DC797C&subkey=1560860&md5=19f331fe239Z HTTP/1.1"
'''
# 按全备类型字典构建数据
category_num ={}    
def requrl_split(log):
    with open(log,"r") as f:    
        for line in f:
            try:
                line=line.split('\"')
                category,info=line[1].split('?')
                category = category.split()[1].replace('/', '')
                data_set={ ckey:"" for ckey in category_fields.get(category) }
                data_set["category"] = category
                
                # 类别汇总
                try:
                    category_num[category] = category_num[category] + 1
                except:
                    category_num[category] = 0

                # 解析请求体
                if not info:continue
                infolist=info.split("&")
                for i in range(0,len(infolist)):
                    if(len(infolist[i])>0) and infolist[i].find('=')!=-1:
                        key,value=infolist[i].split("=")
                        if key in data_set:
                            data_set[key]=value
                
                # 汇总结果(以list的方式保存)
                list_res=[data_set[ckey] for ckey in category_fields.get(category) ]
                fhandle=category_handles.get(category,"unknown")
                print >> fhandle, ','.join(list(map(lambda x : str(x),list_res)))
            except Exception,e:
                t,value,traceback = sys.exc_info()
                print str(e)
                print "\033[1;31m%s\033[0m" %(line)
            finally:
                del data_set
    
# 将类别汇总的结果写入文件（简报的形式,牵涉到字典写成行文件）
def save_category_nums():
    fres=open(stat_res,'a+')
    if not os.path.getsize(stat_res):
        title="%-10s\t"*len(category_num.keys()-1)+"%-10s\r\n" %category_num.keys()
        fres.write(title)

    result="%-10s\t"*len(category_num.keys())+"%-10s\r\n" %(calcday,)
    fres.write(result)
    fres.close()

'''
    Part3: 2.IP和请求时间分割：
    IP和时间格式：27.27.28.235 - - [21/Dec/2016:14:13:01 +0800]
'''
# 根据事先的提取出ip和时间
def iptime_split(log):
    reqfre=defaultdict(int)
    with open(log,"r") as f:
        for line in f:
            try:
                line=line.split('\"')[0].strip()
                # 正则删除中括号re.sub(r'[\[\]]','',line)
                ip,datestr=re.split(r'[- \[]*',line)[:-1]
                hourmin=datestr.split(':')[1]+':'+datestr.split(':')[2]
                reqfre[hourmin]+=1
            except Exception,e:
                print(str(e))
    reqfre['14:25']=60
    print reqfre
    #sorted by value
    print sorted(reqfre.iteritems(),key=lambda asd:asd[1],reverse=True)


# 【增强版】泛化提取IP，域名和时间
def general_extract_info(log):
    with open(log,"r") as f:
        for line in f:
            try:
                ipsearch=re.search(r'\d+.\d+.\d+.\d+ ',line)                  # ip地址
                if ipsearch:
                    print 'find ip:',
                    print ipsearch.group()

                domainsearch=re.search(r'(?<=://)[a-zA-Z\.0-9]+(?=\/)',line)  # 域名提取（只是域名)
                if domainsearch:
                    print 'find domain:',
                    print domainsearch.group(0)

                urlsearch=re.search(r'(?<=://)[a-zA-Z\.\-/0-9]+(?=\/)',line)  # 整个url提取
                if urlsearch:
                    print 'find url:',
                    print urlsearch.group()

                querysearch=re.search(r'(?<=://)([a-zA-Z\.\-/0-9]+)/([a-zA-Z0-9]+)(?=[(.html)\?]?)',line)
                if querysearch:
                    print 'find query:',
                    print querysearch.group()

                hourminsearch=re.search(r'(?<=\[)([0-9]{1,2}\/[A-Z]{1}[a-z]{2}\/[0-9]{4}:)([:0-9]{8})(?=\+0800\])',line)
                if hourminsearch:
                    print 'find hourmin:',
                    print hourminsearch.group(0),hourminsearch.group(1)
            except Exception,e:
                print(str(e))


'''
    测试入口
'''
if __name__ == "__main__":
    #iptime_split(log)
    general_extract_info(log)
    sys.exit()
    # 构造全备类型字典
    build_category_fields(log)
    # 打开类型句柄
    open_category_handles()
    # 请求体分割
    requrl_split(log)
    # 保存类型结果
    save_category_nums()
    # 关闭类型句柄
    close_category_handles()

