#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'yjm'
'''
  功能注释：高潮模式实现
'''

import os, sys
import json,urllib2
import MySQLdb
from collections import OrderedDict

############# 参数设置
pthreshsize=5;	# 调节峰值筛选阈值

############# 全局变量
top_cid_filesize='toplist'						# 待添加高潮模式的影片信息文件列表
datapath='/usr/local/sandai/xmp_hotview/data'   # 原始采集数据文件位置
hotrespath='/usr/local/sandai/xmp_hotview/high' # 高潮模式结果信息文件


############# step0: get viewdata
'''
    首先利用update_top_cidfilesize函数获取播放最多的影片的cid和filesize信息到本地的toplist文件
	或者toplist列表,然后step1根据cid和filesize查找本地文件得到view数据
'''
# 获取cid和filesize信息
def update_top_cidfilesize(top_cid_filesize): 
    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='xmp', passwd='view_hot',db='xmp_hot_view')
    if not conn.open:
        print('open connnection fail')
        exit()
    cur = conn.cursor()
    cur.execute('set names utf8;')

    toplist=[]
    infostr=""
    for i in range(0, 256):
        table='hot_view_%02X' % i
        try:
            sql = "select cid,filesize from {table}  where  view_num>{viewlimit} and duration>{durlimit};".format(table=table,viewlimit=2000,durlimit=600);
            print(sql)
            cur.execute(sql)
            querydatas = cur.fetchall()
            for querydata in querydatas:
            	toplist.append(querydata)
            	infostr+=querydata[0]+'.'+str(querydata[1])+'\n'
        except Exception,e:
            derror=sys.exc_info()
            print "error-->%s,line:%s" %(derror[1],derror[2].tb_lineno)
    cur.close()
    conn.close()

    # 存文件
    fout=open(top_cid_filesize,'w')
    fout.write(infostr)
    fout.close()

	# 返回文件信息列表
    return  toplist;


# 读取本地的文件数据
'''
    利用cid和filesize信息获取view数据（view数据中包含cid和filesize信息）
    readfile ='/usr/local/sandai/xmp_hotview/data/A4/8F/A48FF45C5BF840DA58690BC6EFE5387DF56EF752.1026430435'
'''
def getview_from_local(datapath='/usr/local/sandai/xmp_hotview/data',updateTop=False):
    if updateTop or not os.path.exists(top_cid_filesize):
        update_top_cidfilesize()
    for line in open(top_cid_filesize):
        line=line.strip('\n')
        readfile=os.path.join('/usr/local/sandai/xmp_hotview/data',line[0:2],line[2:4],line)
        print readfile
        rfb = open(readfile)
        try:
            hot_info = rfb.read()
            jsob_body = json.loads(hot_info)
            view = jsob_body.get("hot_view")
            cid, filesize = line.split('.')
            procflow(cid,filesize,view)    #调用了整体实现流程
        except Exception,e:
            s=sys.exc_info()
            print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)
        finally:
            rfb.close()
    return 0;


############# step1:smooth data
# 1.1 输入排序字典，输出排序字典，寻找峰值点
def getpeak(dictview):
    peakmap = {}
    keys=dictview.keys()
    for key, value in dictview.items():
        if key == keys[0] or key == keys[-1]:
            continue
        previouskey=keys[keys.index(key)-1]
        behindkey=keys[keys.index(key)+1]
        if dictview[previouskey] < dictview[key] and dictview[key] > dictview[behindkey]:
            peakmap[key] = value

    # 记录的是原始数据的峰值点坐标（pos,views）
    peeks = OrderedDict([(k, peakmap[k]) for k in sorted(peakmap.keys())])
    return peeks


# 1.2 数据平滑
# 输入列表view，输出排序字典
def smoothdata(timedur,view):
    # 输入数据重新构造
    dictview=OrderedDict()
    for n,view in enumerate(view):
        dictview[n+1]=view

    # 根据影片时长进行平滑
    if (timedur < 300):    # <5min平滑一次
        smdata = getpeak(dictview)
    elif (timedur < 3600): # 5~60min平滑两次
        smdata = getpeak(dictview)
        smdata = getpeak(smdata)
    else:                  # >40min平滑三次
        smdata = getpeak(dictview)
        smdata = getpeak(smdata)
        smdata = getpeak(smdata)
    return smdata;


############# step2: find high_peak
'''
#smdata=[(232,5464),(1634,25346),(45403,4540)]
#dsmdata=[(1634,25346),(45403,4540),(???,avg)]
'''
# 分详细情况实现波峰寻找
def find_high_peek(smdata):
    # step:一阶差分
    smdata=smdata.items()      # 反有序字典
    ori_list=smdata[0:len(smdata)-1]
    cmp_list = smdata[1:]
    onediff_pv = map(lambda x, y:(x[0],y[1] - x[1]), ori_list, cmp_list)

    # step:求波峰
    peeks=[]
    onediff_v=map(lambda x:x[1],onediff_pv)
    threshold = (max(onediff_v) - min(onediff_v)) / pthreshsize

    # 分情况实现
    n=0
    while n<len(onediff_pv):
        ## 正和情况
        psum=0
        if n==0:                            # 情况1:Y(n-1)不存在 and Y(n+m+1)<0
            for k in range(n,len(onediff_pv)):
                if onediff_pv[k][1]>=0:
                    psum+=onediff_pv[k][1]
                else:
                    if psum>=threshold:
                        peeks.append(smdata[k])
                    break
        psum=0                              # 情况2：Y(n-1)<0 and Y(n+m+1)<0
        if onediff_pv[n][1]<0:
            for k in range(n+1, len(onediff_pv) ):
                if onediff_pv[k][1] >= 0:
                    psum += onediff_pv[k][1]
                else:
                    if psum >= threshold:
                        peeks.append(smdata[k])
                    break
        psum=0
        if onediff_pv[n][1]<0:              # 情况3：Y(n-1)<0 and Y(n+m+1)不存在
            for k in range(n+1, len(onediff_pv)):
                if onediff_pv[k][1] >= 0:
                     psum += onediff_pv[k][1]
                     if k==len(onediff_pv)-1:
                         if psum>=threshold:
                             peeks.append(smdata[k+1])
                else:
                    break

        ## 负和情况
        nsum=0
        if n==0:                            # 情况4:Y(n-1)不存在,Y(n+m+1)>0
            for k in range(n,len(onediff_pv)):
                if onediff_pv[k][1]<=0:
                    nsum+=onediff_pv[k][1]
                else:
                    if nsum<=-threshold:
                        peeks.append(smdata[n])
                    break
        nsum=0
        if onediff_pv[n][1]>0:             # 情况5：Y(n-1)>0 and Y(n+m+1)>0
            for k in range(n+1,len(onediff_pv)):
                if onediff_pv[k][1]<=0:
                    nsum+=onediff_pv[k][1]
                else:
                     if nsum<=-threshold:
                        peeks.append(smdata[n+1])
                     break
        nsum=0
        if onediff_pv[n][1]>0:           # 情况6：Y(n-1)>0 and Y(n+m+1)不存在
            for k in range(n+1, len(onediff_pv)):
                if onediff_pv[k][1] <= 0:
                     nsum += onediff_pv[k][1]
                     if k==len(onediff_pv)-1:
                         if nsum<=-threshold:
                             peeks.append(smdata[n+1])
                else:
                    break
        n+=1

    peeks=OrderedDict(sorted(peeks))
    onediff_pv=OrderedDict(onediff_pv)
    return peeks,onediff_pv


############ step3:find high_dur
'''
	peerks和onediff_pv两者均是排序字典:
	peerks=OrderedDict([(21,5464),(1634,25346),(45403,4540)])  
	onediff_pv=OrderedDict([(21,5464),(1634,25346),(45403,4540)])
'''
def find_high_dur(peaks,onediff_pv,smdata):
    smdata=smdata.items() # 反字典化
    high_dur = []
    diffkeys=onediff_pv.keys()
    peakkeys=peaks.keys()

    # 对每个波峰进行左右搜索
    for pos,view in peaks.items():
        #左搜索区间
        if pos==peakkeys[0]:
            lppos=diffkeys[0]
        else:
            lppos=peakkeys[peakkeys.index(pos)-1]  # 左峰时间点
        lsdur=filter(lambda x:x>=lppos and x<pos,diffkeys)

        #右搜索区间
        if pos==peakkeys[-1]:
            rppos=diffkeys[-1]
        else:
            rppos=peakkeys[peakkeys.index(pos)+1] # 右峰时间点
        rsdur=filter(lambda x:x>pos and x<=rppos,diffkeys)

        #进行搜素
        startp=-1
        endp=-1
        for dkey in lsdur[::-1]:
           if onediff_pv[dkey]<0:    # 左寻找
                adkey=diffkeys[diffkeys.index(dkey)+1] #波峰点和差分的后一个点的
                startp=(pos+adkey)/2 #*0.99
                break
           if dkey==lsdur[0]:        # 若遍历没有找到（则把左边第一个点作为高潮起点）
               startp=(smdata[0][0]+pos)/2

        for dkey in rsdur:
            if onediff_pv[dkey]>0:  # 右寻找
                adkey=diffkeys[diffkeys.index(dkey)]
                endp=(pos+adkey)/2  #*1.01
                break
            if dkey==rsdur[-1]:     #若变量没有找到
                endp=(smdata[-1][0]+pos)/2

        # 区间搜索情况
        if startp!=-1 and endp!=-1:     # 左右区间都搜索到
            high_dur.append((startp,endp))
        elif startp==-1 and endp!=-1:  # 搜索到右区间
            high_dur.append((pos,endp))
        elif startp!=-1 and endp==-1:  # 搜索到左区间
            high_dur.append((startp,pos))

    return high_dur;

#step3.1  高潮区间合并
'''
	将小于5的删除，将区间间隔小于5的合并（这里还存在提升空间）
'''
def mergehigh(high_dur):
    hdurbg5=filter(lambda x:x[-1]-x[0]>5,high_dur)
    if not hdurbg5:
        return high_dur

    hdurmerge=[]
    mergelast=False
    try:
        for n in range(0,len(hdurbg5)-1):
            if hdurbg5[n+1][0]-hdurbg5[n][-1]<5:
                mdur=(hdurbg5[n][0],hdurbg5[n+1][-1])
                hdurmerge.append(mdur)
                if n==len(hdurbg5)-2:
                    mergelast=True
            else:
                hdurmerge.append(hdurbg5[n])
        if not mergelast:                       # 将最后未合并的末尾区间统计进来
            hdurmerge.append(hdurbg5[-1])
    except Exception,e:
        s=sys.exc_info()
        print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)

    return hdurmerge;

#step3.2  判断高潮区间的占比
'''
	占全片的比例小于20%或者大于80%，提交审核
'''
def judgehigh(highdur,view):
    flag=''
    totoal_high=sum(map(lambda x:x[-1]-x[0],highdur))
    if totoal_high<0.2*len(view):
        print "highdur too less(<%20)"
        flag='highdur too less(<%20)'
    elif totoal_high>0.8*len(view):
        print "highdur too much(>80%)"
        flag='highdur too much(>80%)'
    else:
        print "highdur OK!"
        flag='ok'

    return flag


########### step4: save result
#higdur=[(123,205),(232,256),....(278,400)]
def savehigh(cid,filesize,highdur,hotrespath='/usr/local/sandai/xmp_hotview/high'):
    fisrtpath=cid[0:2]
    secondpath=cid[2:4]
    fpath=os.path.join(hotrespath,fisrtpath,secondpath)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    fname=os.path.join(fpath,cid+str(filesize))
    f=open(fname,'w')
    highstr=map(lambda x:str(x[0])+"_"+str(x[1]),highdur)
    highdur_dict={}
    highdur_dict['highdur']=highstr
    json.dump(highdur_dict,f)
    f.close()


# 数据处理流程
def procflow(cid,filesize,view):
    #step1:获取影片时长
    timedur= len(view) 

    #step2: 数据平滑
    smdata = smoothdata(timedur, view)
    if not smdata:
        return -1

    #step3:获取高潮点
    peaks, onediff = find_high_peek(smdata)
    if not peaks or not onediff:
        return -2

    #step4:获取初始高潮区间
    high = find_high_dur(peaks, onediff,smdata)
    if not high:
        return -3

    #step5 合并和判断高潮区间
    merhigh=mergehigh(high)
    #flag=judgehigh(merhigh,view)
    #if flag!='ok':
    #    return -4

    #step6:保存高潮区间
    hotrespath="/home/yjunmiao"
    savehigh(cid,filesize,merhigh,hotrespath)

###################### 测试区
def test_whole():
    '''
    0E93E1D1A1271E6271F1CDA4E73FBC9F332D66BB.388523367
    028F6087180684CBE72CD19B35ACAC8FC8ABC4D5.2319407843
    12E9CD43D00C33A0DBA1916B23EDF3DC0F095561.2413207732
    182C18362D55FC93897CC236D1BEA5C8287BF61A.968055719
    '''
    c= '''
    1288B6AAAF492077749DDAEAF33348259BD10981.2470630706
    '''

    filelist=map(lambda x:x.strip(),c.strip().split('\n'))
    
    for i in filelist:
        readfile=os.path.join('/usr/local/sandai/xmp_hotview/data',i[0:2],i[2:4],i)
        rfb = open(readfile)
        try:
            hot_info = rfb.read( )
        finally:
            rfb.close( )
        json_body = json.loads(hot_info)
        view = json_body.get("hot_view")
        fname = os.path.split(readfile)[1]
        cid, filesize = fname.split('.')
        print readfile
        procflow(cid,filesize,view)
    
    return 0

if __name__ == "__main__":
    if len(sys.argv) ==1:
        test_whole()
        #getview_from_local(datapath)
    elif len(sys.argv)==2:
        updateTop=False
        if sys.argv[1]=='update':
            updateTop=True
        else:
            print "useage:\n %s update \n\t to get the latest fileinfo\n" %(sys.argv[0])
            getview_from_local(datapath,updateTop)
    else:
        print "please check parameters"
        exit()



