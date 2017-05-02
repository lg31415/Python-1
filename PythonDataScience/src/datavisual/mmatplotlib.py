#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能：Python数据可视化：matplotlib实现
  参考：http://www.shareditor.com/blogshow/?blogId=55
       http://www.toutiao.com/i6410597836664078849/
       http://matplotlib.org/examples
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
    基本使用
'''
def basic_plot():
    # 多维数组
    '''
    ldata=[1,2,7,3,8,4,5,5,6,10]
    ndata=np.array(ldata)
    plt.plot(ndata,np.sin(ndata),'--',linewidth=2,color='red')
    plt.show()
    '''

    x=[2,5,3,42,1,5]
    y1=[23,34,3,54,64,1]
    y2=[ v*np.sin(v) for v in y1]

    # 折线图
    '''
    plt.figure()
    plt.plot(x,y1,'o')
    plt.plot(x,y2,'--',linewidth=2,color='red')
    plt.xlabel(u'x轴')
    plt.ylabel(u'y轴(y1,y2)')
    plt.title(u'标题')
    plt.show()
    '''

    # 柱状图
    '''
    plt.figure()
    plt.bar(x,y1)
    plt.show()
    '''

    # 饼图
    plt.figure()
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 150]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=False, startangle=90,pctdistance=0.6)
    plt.axis('equal')         # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


'''
    中级使用
'''
def medium_plot():
    #子图
    x=range(5)
    y1=[v+2 for v in x ]
    y2=[v+3 for v in x ]
    plt.figure()

    '''
    plt.subplot(211)
    plt.plot(x,y1)
    plt.xlabel('xsub1')
    plt.ylabel('ysub1')
    plt.title('titlesub1')

    plt.subplot(212)
    plt.plot(x,y2)
    plt.xlabel('xsub2')
    plt.ylabel('ysub2')
    plt.title('titlesub2')
    plt.show()
    '''

    #图例
    plt.plot(x,y1,label='tu1')
    plt.plot(x,y2,label='tu2')
    plt.legend()
    plt.show()



'''
    实战应用
'''
#绘图和标注(smdata,onediff都是OrderDict)
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
    #plt1 = plt.subplot(2,2,1) # 在一张图上绘制多个子图


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

    return 0


# 条形图的绘制
def draw_bar():
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
    y_pos = np.arange(len(people))
    performance = 3 + 10 * np.random.rand(len(people))
    error = np.random.rand(len(people))

    ax.barh(y_pos, performance, xerr=error, align='center',color='green', ecolor='red')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Performance')
    ax.set_title('How fast do you want to go today?')

    plt.show()



# 测试入口
if __name__ == "__main__":
    basic_plot()
    #medium_plot()
    #draw_bar()
