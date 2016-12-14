#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：计算简单移动平均和指数移动平均
  Improve:
        1,先拟合，再平滑
        2，
'''

import os,sys
import numpy as np
import json
import matplotlib.pyplot as plt


data=np.loadtxt('../data/smdata',delimiter=',',unpack=True)
N=20;
t=np.arange(N-1,data.size)
smdata=[]
print(type(data))

############## step1:smoooth & polyfit
'''
    移动平均综合测试
'''
def smavg():
    # 权重设置
    weights_exp=np.exp(np.linspace(-1,0,N))
    weights_exp/=weights_exp.sum()
    weights_sim=np.ones(N)
    weights_sim/=weights_sim.sum()
    weights_blw=np.blackman(N)
    weights_blw/=weights_blw.sum()

    # 平滑操作
    sm_exp=np.convolve(weights_exp,data)[N-1:-N+1]
    sm_sim=np.convolve(weights_sim ,data)[N-1:-N+1]
    sm_blw=np.convolve(weights_blw ,data)[N-1:-N+1]

    #np.savetxt('result',expa)
    exp_mean=1.01*np.average(sm_exp)
    sim_mean=1.02*np.average(sm_sim)

    #sub mean
    #expa=expa-exp_mean
    #sima=sima-sim_mean

    # 绘图
    #plt.plot(t,data[N-1:],lw=1.0)
    #plt.figure()
    plt.plot(t,data[N-1:],'k',label='origin')
    #plt.plot(t,sm_exp,'r',label='exp avg') #指数移动平均
    #plt.plot(t,sm_sim,'g',label='sim avg') #简单移动平均
    plt.plot(t,sm_blw,'y',lw=2.0,label='blackman win avg')  #布莱克曼窗函数
    plt.legend(loc='upper center')

    #plt.axhline(y=exp_mean,lw=2,color='y')
    #plt.axhline(y=sim_mean,lw=2,color='b')
    plt.show()

'''
    窗平均单独测试
'''
def win_avg():
    N=20
    weights=np.blackman(N)
    weights/=weights.sum()

    avg_bmw=np.convolve(weights,data)[N-1:-N+1]
    plt.plot(t,avg_bmw,lw=1.0,color='r')
    plt.main('blackman')
    plt.show()

'''
    局部回归多项式拟合：开发中(已用R实现)
'''
def  polyfit():
    #进行曲线拟合
    order=9
    xa=np.arange(data.size)
    ya=data

    matA=[]
    for i in range(0,order+1):
        matA1=[]
        for j in range(0,order+1):
            tx=0.0
            for k in range(0,len(xa)):
                dx=1.0
                for l in range(0,j+i):
                    dx=dx*xa[k]
                tx+=dx
            matA1.append(tx)
        matA.append(matA1)

    #print(len(xa))
    #print(matA[0][0])
    matA=np.array(matA)

    matB=[]
    for i in range(0,order+1):
        ty=0.0
        for k in range(0,len(xa)):
            dy=1.0
            for l in range(0,i):
                dy=dy*xa[k]
            ty+=ya[k]*dy
        matB.append(ty)

    matB=np.array(matB)

    matAA=np.linalg.solve(matA,matB)

    #画出拟合后的曲线
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #print(matAA)
    xxa= np.arange(-1,1.06,0.01)
    yya=[]
    for i in range(0,len(xxa)):
        yy=0.0
        for j in range(0,order+1):
            dy=1.0
            for k in range(0,j):
                dy*=xxa[i]
            dy*=matAA[j]
            yy+=dy
        yya.append(yy)

    ax.plot(xxa,yya,color='g',linestyle='-',marker='')
    ax.legend()
    plt.show()



if __name__ == "__main__":
	smavg()
