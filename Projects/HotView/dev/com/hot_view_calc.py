#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'yjm'
'''
  功能注释：高潮模式实现
'''

import os, sys
import numpy as np
import json,urllib2
import matplotlib.pyplot as plt
import MySQLdb
from collections import OrderedDict

############# 参数设置
pthreshsize=5;    # 调节峰值筛选阈值

############# step0: get viewdata
# 预处理:从网络获取最新的cid,filesize的view数据(得到toplist)
'''
    首先利用update_top_cidfilesize函数获取播放最多的影片的cid和filesize信息到本地的toplist文件，然后根据cid和filesize拼接url信息，利用urlib2得到view数据
'''
top_cid_filesize='toplist'
def update_top_cidfilesize(top_cid_filesize): # 获取cid和filesize信息
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
            sql = "select cid,filesize from {table}  order by view_num desc limit 1;".format(table=table);
            print(sql)
            cur.execute(sql)
            querydata = cur.fetchone()
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
    return  toplist;


# method1:直接获取网络数据（根据toplist）
def getview_from_web(top_cid_filesize='toplist',update=False):
    if update:
        update_top_cidfilesize()  # 更新最高播放排行的cid和filesize到本地的toplist文件
    try:
        for line in open(top_cid_filesize):
            cid,filesize=line.strip().split('.')
            url="http://hotview.v.xunlei.com/"+cid[0:2]+"/"+cid[2:4]+"/"+cid+"."+filesize
            resonse=urllib2.urlopen(url)
            content=resonse.read().decode('utf8')
            viewdata=json.loads(content)
            views=viewdata.get('hot_view','')
            if views:
                #return  cid,filesize,views
                procflow(cid,filesize,views)
    except Exception,e:
        s=sys.exc_info()
        print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)
    return 0;

# method2:part0 获取网络数据保存本地（根据toplist）
'''
    利用cid和filesize信息将view数据保存到本地（view数据中包含cid和filesize信息）
    readfile ='D:\\hot_data\\A4\\8F\\A48FF45C5BF840DA58690BC6EFE5387DF56EF752.1026430435' #sys.argv[1]
'''
def saveview_to_local(top_cid_filesize='toplist',datapath='D:\\hot_data',update=False):
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    if update:
        update_top_cidfilesize()  # 更新最高播放排行的cid和filesize到本地的toplist文件
    try:
        for line in open(top_cid_filesize):
            cid,filesize=line.strip('\n').split('.')
            url="http://hotview.v.xunlei.com/"+cid[0:2]+"/"+cid[2:4]+"/"+cid+"."+filesize
            resonse=urllib2.urlopen(url)
            content=resonse.read().decode('utf8')
            #viewdata=json.loads(content)
            #json.dump(viewdata)
            fpath=os.path.join(datapath,cid[0:2],cid[2:4])
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            fname=os.path.join(fpath,line.strip('\n'))
            fout=open(fname,'w')
            fout.write(content)
            fout.close()
    except Exception,e:
        s=sys.exc_info()
        print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)

    return 0;

# method2:part1 获取本地数据（根据toplist）
def getview_from_local(datapath='D:\\hot_data'):
    if not os.path.exists(datapath):
        saveview_to_local()
    for root, dirs, files in os.walk(datapath):
        for file in files:
            readfile= os.path.join(root, file)
            fname = os.path.split(readfile)[1]
            rfb = open(readfile)
            try:
                hot_info = rfb.read()
                jsob_body = json.loads(hot_info)
                view = jsob_body.get("hot_view")
                cid, filesize = fname.split('.')
                procflow(cid,filesize,view)
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


'''
# 坐标系转换
fgview = [(12, 2323), (15, 2345), (324, 23045), (1324, 443543)]  # 1,输出点坐标
tmp = [2323, 2345, 23045, 443543]  # 输出点抽取
bgview = [(1, 2325), (3, 23045)]
true_bgview = [(12, 2323), (324, 23045)]  # 对输出的坐标都是原始数据的坐标点

def coortransform(fgview, bgview):
    mapview = []
    for item in range(len(bgview)):
        mappos = bgview[item][0]
        truepos = fgview[mappos][0]
        newpv = (truepos, bgview[item][1])
        mapview.append(newpv)
    return mapview;
'''
# 1.2 查询影片时长
def getduration(cid,filesize):
    conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='xmp', passwd='view_hot',db='xmp_hot_view')  #新建的数据库
    if not conn.open:
        print('open connnection fail')
        sys.exit()
    cur = conn.cursor()
    cur.execute('set names utf8;')

    try:
        table ='hot_view'+cid[0:2]
        sql = "select duration from {table} where cid={cid} and fileszie={filesize}".format(table=table,cid=cid,filesize=filesize);
        print(sql)
        cur.execute(sql)
        querydata = cur.fetchone()
        timedur = querydata[0]
    except Exception,e:
        derror=sys.exc_info()
        print "error:{},line:{}".format(derror[1],derror[2].tb_lineno)
    finally:
        cur.close()
        conn.close()

    return timedur;

# 1.3数据平滑
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
def find_high_peek(smdata):
    if not smdata:
        print "smooth no point"
        exit()
    # step:一阶差分
    smdata=smdata.items() # 反有序字典
    ori_list=smdata[0:len(smdata)-1]
    cmp_list = smdata[1:]
    onediff_pv = map(lambda x, y:(x[0],y[1] - x[1]), ori_list, cmp_list)

    # step2:寻找峰值
    peeks = []
    onediff_v=map(lambda x:x[1],onediff_pv)
    threshold = (max(onediff_v) - min(onediff_v)) / pthreshsize

    '''
    # 首先进行最值查找
    peek1 = [ v for v in onediff_pv if v[1] < -threshold ]  #
    peeks.extend(peek1)
    peek2 = [ onediff_pv[n + 1] for n, v in enumerate(onediff_pv) if v[1] >threshold]
    peeks.extend(peek2)
    '''

    '''
    # 第一次查找（穹顶和凹陷）
    n = 0
    while  n< len(onediff_pv):
        wsum = 0
        if onediff_pv[n][1]<0:
            for k in range(n+1, len(onediff_pv) ):
                if onediff_pv[k][1] >= 0:
                    wsum += onediff_pv[k][1]
                else:
                    if wsum > threshold:
                        peeks.append(smdata[k])
                    break

        wsum = 0
        if onediff_pv[n][1]>0:
            for k in range(n+1, len(onediff_pv)):
                if onediff_pv[k][1] <= 0:
                    wsum += onediff_pv[k][1]
                else:
                    if wsum <-threshold:
                        peeks.append(smdata[n+1])
                    break

        n+=1

    # 第二次查找（最大子序列）严格要求两侧的边界存在
    n=0
    while  n< len(onediff_pv):
        if onediff_pv[n][1]<=0:
            negativesum=0
            for k in range(n+1, len(onediff_pv)):   # 避免单值
                if onediff_pv[k][1]<0:
                    negativesum+=onediff_pv[k][1]
                    if negativesum<-threshold:
                        peeks.append(smdata[n])    # 将连负的起点作为峰值点
                        break
                else:
                    if negativesum<-threshold:
                        peeks.append(smdata[n])   # 将连负的起点作为峰值点
                    break

        if onediff_pv[n][1]>=0:
            positivesum=0
            for k in range(n+1, len(onediff_pv)):  # 避免单值
                if onediff_pv[k][1]>0:
                    positivesum+=onediff_pv[k][1]
                    if positivesum>threshold:
                        peeks.append(smdata[k]) # 将连正的尾点作为峰值点
                        break
                else:
                    if positivesum>threshold:
                        peeks.append(smdata[k]) # 将连正的尾点作为峰值点
                    break
        n+=1
    '''
    # 对第二次查找的改进（不严格要求两侧的边界存在）
    n=0
    while  n< len(onediff_pv):
        psum=0
        if n-1<0 or onediff_pv[n-1][1]<0:         # 当前差分正序列点的前一点不存在，或者小于0
            for k in range(n,len(onediff_pv)):
                if onediff_pv[k][1]>=0:
                    psum+=onediff_pv[k][1]
                    if k==len(onediff_pv)-1:      # 加这个判断是防止提前退出，包含到最后一点（差分不存在）
                        if psum>=threshold:
                            peeks.append(smdata[k+1])
                            break
                else:                             # 差分小于0
                    if psum>=threshold:
                        peeks.append(smdata[k])
                    break
        nsum=0
        if n-1<0 or onediff_pv[n-1][1]>0:         # 当前差分负序列点的前一点不存在，或者大于0
            for k in range(n,len(onediff_pv)):
                if onediff_pv[k][1]<=0:
                    nsum+=onediff_pv[k][1]
                    if k==len(onediff_pv)-1:      # 加这个判断是防止提前退出，包含到最后一点（差分不存在）
                        if nsum<=-threshold:
                            peeks.append(smdata[n])
                            break
                else:                             # 差分大于0
                    if nsum<=-threshold:
                        peeks.append(smdata[n])
                    break
        n+=1

    peeks=OrderedDict(sorted(peeks))
    onediff_pv=OrderedDict(onediff_pv)
    return peeks,onediff_pv

# 分详细情况实现波峰寻找
def find_high_peek_tmp(smdata):
    if not smdata:
        print "smooth no point"
        return {},{}
    # step:一阶差分
    smdata=smdata.items() # 反有序字典
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
# 两者均是排序字典
# peerks=OrderedDict([(21,5464),(1634,25346),(45403,4540)])  #遍历
# onediff_pv=OrderedDict([(21,5464),(1634,25346),(45403,4540)])
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
           if onediff_pv[dkey]<0:  # 左寻找
                adkey=diffkeys[diffkeys.index(dkey)+1] #波峰点和差分的后一个点的
                startp=(pos+adkey)/2 #*0.99
                break
           if dkey==lsdur[0]:     # 若遍历没有找到（则把左边第一个点作为高潮起点）
               startp=(smdata[0][0]+pos)/2

        for dkey in rsdur:
            if onediff_pv[dkey]>0:  # 右寻找
                adkey=diffkeys[diffkeys.index(dkey)]
                endp=(pos+adkey)/2 #*1.01
                break
            if dkey==rsdur[-1]:  #若变量没有找到
                endp=(smdata[-1][0]+pos)/2

        # 区间搜索情况
        if startp!=-1 and endp!=-1:     # 左右区间都搜索到
            high_dur.append((startp,endp))
        elif startp==-1 and endp!=-1:  # 搜索到右区间
            high_dur.append((pos,endp))
        elif startp!=-1 and endp==-1:  # 搜索到左区间
            high_dur.append((startp,pos))

    return high_dur;

# 高潮区间合并
# 将小于5的删除，将区间间隔小于5的合并
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
        if not mergelast:                       # 将最后未合并的区间统计进来
            hdurmerge.append(hdurbg5[-1])
    except Exception,e:
        s=sys.exc_info()
        print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)

    return hdurmerge;

# 判断高潮区间的占比
# 占全片的比例小于20%或者大于80%，提交审核
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
def savehigh(rootpath,cid,filesize,highdur):
    fisrtpath=cid[0:2]
    secondpath=cid[2:4]
    fpath=os.path.join(rootpath,fisrtpath,secondpath)
    if not os.path.exists(fpath):
        os.makedirs(fpath)           #创建结果目录
    fname=os.path.join(fpath,cid+'.'+str(filesize))
    f=open(fname,'w')
    highstr=map(lambda x:str(x[0])+"_"+str(x[1]),highdur)
    highdur_dict={}
    highdur_dict['highdur']=highstr
    json.dump(highdur_dict,f)
    f.close()


########### step5: draw high
#smdata,onediff都是OrderDict
def drawhigh(view,onediff,smdata,peeks,high,cid,filesize,flag):
    smdata_x=map(lambda x:x[0],smdata.items())
    smdata_y=map(lambda x:x[1],smdata.items())
    onediff_x=map(lambda x:x[0],onediff.items())
    onediff_y=map(lambda x:x[1],onediff.items())
    peeks_x=map(lambda x:x[0],peeks.items())
    peeks_o=map(lambda x:x[1],peeks.items())

    # 差分统计
    mean_onediffv=sum(onediff_y)/len(onediff_y)
    max_onediffv=max(onediff_y)
    min_onediffv=min(onediff_y)
    threshhold=(max_onediffv-min_onediffv)/5

    # 求波峰点的差分数据
    peeks_diff=[]
    for p in peeks_x:
        if onediff.has_key(p):
            peeks_diff.append(onediff[p])
        elif p==smdata_x[-1]:
            peeks_diff.append(smdata_y[-1])  # smdata最后一点是波峰点，但没有差分数据,用原始数据代替差分数据
        else:
            print "wrong peek find"
            exit()

    # 图像设置
    plt.figure(figsize=(15,7))  # figsize()设置的宽高比例是是15:7，图片的尺寸会根据这个比例进行调节
    #plt.xlim(-3,19)
    lowlimit=min(onediff_y)-500 #y轴下限
    highlimit=max(view)+500     #y轴上限
    plt.ylim(lowlimit,highlimit)
    plt.grid(which='both')


    #绘制结果数据
    plt.plot(range(1,len(view)+1),view,color='y',lw=0.5,label='origin')  # 原始图像
    plt.plot(smdata_x,smdata_y,'ro-',ms=3,label='smooth')                # 平滑后的数据
    plt.plot(onediff_x,onediff_y,'go-',ms=3,label='onediff')             # 一阶差分
    plt.plot(peeks_x,peeks_o,'r^',ms=9,label='peak')                     # (原曲线上）绘制峰
    plt.plot(peeks_x,peeks_diff,'g^',ms=9,label='diff_peak')             # (差分线上) 绘制峰,差分线的最后一点
    plt.legend(loc='upper right')
    plt.xlabel('time (s)')
    plt.ylabel('views')
    plt.title(flag)

    # 差分线标注
    plt.axhline(y=max_onediffv,lw=1,ls='-.',color='r')  # 差分上限
    plt.axhline(y=min_onediffv,lw=1,ls='-.',color='r')  # 差分下限
    plt.axhline(y=mean_onediffv,lw=1,ls='-.',color='r') # 差分均值
    plt.axhline(y=threshhold,lw=2,ls='--',color='b')    # 差分上阈值
    plt.axhline(y=-threshhold,lw=2,ls='--',color='b')   # 差分下阈值
    plt.axhline(y=0,lw=2,color='k')


    # 标注高潮区间
    for item in high:
        #plt.axvline(x=item[0],lw=2)
        #plt.axvline(x=item[1],lw=2)
        plt.annotate('',xy=(item[1],1000),xytext=(item[0],1000),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
        plt.fill_betweenx([lowlimit,highlimit],item[0], item[1], linewidth=1, alpha=0.2, color='r')

    plt.show()

    # 结果保存
    '''
    despath='D:\\hot_pic1'
    if not os.path.exists(despath):
        os.makedirs(despath)
    fname=os.path.join(despath,cid+'.'+str(filesize)+'.jpg')
    print fname
    plt.savefig(fname,dpi = 300)
    plt.close()
    '''

    return 0;


# 数据处理流程
def procflow(cid,filesize,view):
    #step1:获取影片时长
    timedur= len(view) #getduration(cid,filesize)

    #step2: 数据平滑(smdata有序字典)
    smdata = smoothdata(timedur, view)
    if not smdata:
        print "-1"
        return -1

    #step3:获取高潮点（peaks和onediff有序字典）
    peaks, onediff = find_high_peek_tmp(smdata)
    if not peaks or not onediff:
        print "-2"
        return -2

    #step4:获取初始高潮区间（high是元组列表）
    high = find_high_dur(peaks, onediff,smdata)
    if not high:
        print "-3"
        return -3

    #step4.1 合并高潮区间（merghigh是元组列表）
    merhigh=mergehigh(high)

    #step4.2 判断高潮区间
    flag=judgehigh(merhigh,view)
    #if flag!='ok':
    #    return 0

    #step5:保存高潮区间
    #rootpath="/home/luochuan/xmp_hotview/hotdata"
    #savehigh(rootpath,cid,filesize,merhigh)

    #step6:展示高潮区间（含中间过程）
    drawhigh(view,onediff,smdata,peaks,high,cid,filesize,flag)


###################### 测试区
# 测试平滑函数
def test_getpeak():
    view={1:12,2:13,3:11,4:15,5:12,6:14,7:4}
    dictview=OrderedDict()
    for n,v in enumerate(view):
        dictview[n+1]=v
    print "origin:",dictview
    res1=getpeak(dictview)
    print "smooth1:",res1.items()
    res2=getpeak(res1)
    print "smooth2:",res2.items()
    return ;

# 测试波峰寻找函数
def test_find_peak():
    smdata=[(1,1),(2,2),(3,4)]
    find_high_peek_tmp(smdata)
    return 0;


# 单项测试
def test_whole():
    '''
    0E93E1D1A1271E6271F1CDA4E73FBC9F332D66BB.388523367
    028F6087180684CBE72CD19B35ACAC8FC8ABC4D5.2319407843
    12E9CD43D00C33A0DBA1916B23EDF3DC0F095561.2413207732
    182C18362D55FC93897CC236D1BEA5C8287BF61A.968055719
    0E93E1D1A1271E6271F1CDA4E73FBC9F332D66BB.388523367
    028F6087180684CBE72CD19B35ACAC8FC8ABC4D5.2319407843
    12E9CD43D00C33A0DBA1916B23EDF3DC0F095561.2413207732
    182C18362D55FC93897CC236D1BEA5C8287BF61A.968055719
    '''
    c= '''
    81046E834BE6420741DAFC3799BB01902219A57E.779309708
    '''
    filelist=map(lambda x:x.strip(),c.strip().split('\n'))
    local=True
    if  local:
        # 获取本地数据
        for i in filelist:
            readfile=os.path.join('D:\\hot_data',i[0:2],i[2:4],i)
            rfb = open(readfile)
            try:
                hot_info = rfb.read( )
            finally:
                rfb.close( )
            json_body = json.loads(hot_info)
            view = json_body.get("hot_view")
            fname = os.path.split(readfile)[1]
            cid, filesize = fname.split('.')
            procflow(cid,filesize,view)
    else:
        #获取网络数据
        for line in filelist:
            cid,filesize=line.strip('\n').split('.')
            url="http://hotview.v.xunlei.com/"+cid[0:2]+"/"+cid[2:4]+"/"+cid+"."+filesize
            resonse=urllib2.urlopen(url)
            content=resonse.read().decode('utf8')
            viewdata=json.loads(content)
            view=viewdata.get('hot_view')
            procflow(cid,filesize,view)

    return 0;

if __name__ == "__main__":
    # 参数检验和信息获取
    if len(sys.argv) ==1:
        test_whole()
        #getview_from_local()
    elif len(sys.argv)==2:
        if sys.argv[1]=='web':
            getview_from_web()
        elif sys.argv[1]=='local':
            getview_from_local()
        else:
            print "please choose [web] or [local]"
            exit()
    else:
        print "please check parameters"
        exit()



