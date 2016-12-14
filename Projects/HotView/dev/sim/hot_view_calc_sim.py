#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：
'''

import os,sys
import json
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np

#阈值调整
adjustv=1.2

# 计算阈值和上下限区间(最后乘以调整系数)
def getthresh_box(lview):
    #view字典化
    dview=OrderedDict()
    for n,view in enumerate(lview):
        dview[n+1]=view
    slview=sorted(lview)
    medianv=np.median(slview)  # 求中位数
    per25=slview[len(slview)/4]
    per75=slview[3*len(slview)/4]
    quardist=per75-per25
    lowlimit=per25-1.5*quardist
    highlimit=per75+1.5*quardist

    fview=filter(lambda x:x<highlimit and x>lowlimit,slview)
    threshold=adjustv*sum(fview)/len(fview)    #加入阈值调整系数,保证至少10%点是高潮点
    if threshold>slview[int(0.9*len(slview))]:
        threshold=slview[int(0.9*len(slview))]
    else:
        pass

    v=[threshold,lowlimit,highlimit]
    return v

# 通过均值调整来实现阈值
def getthresh_mean(lview):
    #view字典化
    dview=OrderedDict()
    for n,view in enumerate(lview):
        dview[n+1]=view
    slview=sorted(lview)  # 排序列表
    threshold=adjustv*sum(lview)/len(lview)

    # 保证至少有10%的高潮
    if threshold>slview[int(0.9*len(slview))]:
        threshold=slview[int(0.9*len(slview))]
    else:
        pass

    return threshold



# 移动均值阈值
def getthresh_move(lview):
    pass



# 求解高潮区间
def gethigh(lview,threshold):
    # view字典化
    dview=OrderedDict()
    for n,view in enumerate(lview):
        dview[n+1]=view

    # 具有高视值的点
    # hview=[(k,v) for k,v in dview.items() if v>avgview*adjustv]
    hviewp=[]
    tmpv=[]
    for i,view in enumerate(lview):
        if view>threshold:
            tmpv.append(i)
        elif tmpv:
            hviewp.append(tmpv)
            tmpv=[]
        else:
            pass
    hdur=filter(lambda x:len(x)>5,hviewp)
    if not hdur:
        return hdur

    hdurm=[]
    mergelast=False
    try:
        for n in range(0,len(hdur)-1):
            if hdur[n+1][0]-hdur[n][-1]<5:
                mdur=hdur[n][:]
                mdur.extend(hdur[n+1])
                hdurm.append(mdur)
                if n==len(hdur)-2:
                    mergelast=True
            else:
                hdurm.append(hdur[n])
        if not mergelast:   # 将最后最长的区间给统计进来
            hdurm.append(hdur[-1])
    except Exception,e:
        s=sys.exc_info()
        print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)

    return  hdurm;

# 绘制高潮区间
def drawhigh(cid,filesize,view,threshold,high,lowlimit=0,highlimit=0):
    avgview=sum(view[5:-5])/len(view)
    highdur=map(lambda x:(x[0],x[-1]),high)

    # 图像设置
    plt.figure(figsize=(15,7)) # figsize()设置的宽高比例是是15:7，图片的尺寸会根据这个比例进行调节
    #plt.xlim(-3,19)
    ylow=min(view)-500      #y轴下限
    yhigh=max(view)+500     #y轴上限
    plt.ylim(ylow,yhigh)
    plt.grid(which='both')


    #绘制结果数据
    plt.plot(range(1,len(view)+1),view,'bo-',ms=1,lw=0.5,label='origin')      # 原始图像
    if lowlimit and highlimit:
        plt.axhline(y=lowlimit,lw=3,ls='-',color='m',label='lowlimit')        # 低限
        plt.axhline(y=highlimit,lw=3,ls='-',color='m',label='highlimit')      # 高限

    plt.axhline(y=avgview,lw=1,ls='--',color='b',label='mean')                # 均值
    #plt.axhline(y=avgview*adjustv,lw=1,ls='--',color='g',label='mean*1.2')   # 均值*adjustv
    plt.axhline(y=threshold,lw=2,ls='--',color='r',label='threshold=1.2*mean')       # 阈值
    plt.legend(loc='upper right')
    plt.xlabel('time (s)')
    plt.ylabel('views')

    # 标注高潮区间
    for item in highdur:
        #plt.axvline(x=item[0],lw=2)
        #plt.axvline(x=item[1],lw=2)
        plt.annotate('',xy=(item[1],threshold),xytext=(item[0],threshold),arrowprops=dict(arrowstyle="->",connectionstyle="arc3",color='g'))
        plt.fill_betweenx([ylow,yhigh],item[0], item[1], linewidth=1, alpha=0.2, color='r')

    plt.show()

    # 结果保存
    '''
    resultpath='D:\\hot_pic2'
    if not os.path.exists(resultpath):
        os.mkdir(resultpath)
    fname=os.path.join(resultpath,cid+'.'+str(filesize)+'.jpg')
    print fname
    plt.savefig(fname,dpi = 300)
    plt.close()
    '''
    return 0;


# 简单计算：从本地读取数据，然后进行计算
def get_from_local(datapath='D:\\hot_data'):
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
                #threshold=getthresh_mean(view)
                threshold,lowlimit,highlimit=getthresh_box(view)  # 增强版计算的阈值
                high=gethigh(view,threshold)
                drawhigh(cid,filesize,view,threshold,high)
            except Exception,e:
                s=sys.exc_info()
                print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)
            finally:
                rfb.close()
    return 0;


#总体测试
def test_whole():
    c= '''
    006C2F93F64D0D7C4D5CD2A0152EF5B8873A74E4.416730555
    '''
    filelist=map(lambda x:x.strip(),c.strip().split('\n'))
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
        view_cid_fz=getthresh(view)
        high=gethigh(cid,filesize,view,view_cid_fz[0])
        drawhigh(view,high,cid,filesize,view_cid_fz)
    return 0

if __name__ == "__main__":
    #test_whole()
    get_from_local()
