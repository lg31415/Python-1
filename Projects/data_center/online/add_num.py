#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：数据中心网页版查询
'''
import os
import sys
import web
import json
import traceback

import matplotlib.pyplot as plt  


'''
    模板操作:
    1,传递的参数渲染到html模板中去，实现html操作python的功能
'''

class Handler:
    # 处理Get请求
    def GET(self):
        web.ctx.status = "200"
        print 'ok'
        params = web.input(cid =None, filesize=0)
        cid = params["cid"]
        filesize = params["filesize"]
        try:
            res=self.dbquery(cid,filesize)
            render = web.template.render('templetes/')
        except ValueError:
            traceback.print_exc()
            return "params type error!"
        
        return  render.dbquery(res)
        
    # 处理post请求的数据
    def POST(self,paras):
        web.ctx.status="400"
        #data=web.data() # 也可以使用这种方法
        paras=web.input(cid=None,filesize=0)
        cid=paras["cid"]
        filesize=paras["filesize"]
        print cid,filesize
        return  u"这是post的返回结果：".encode('utf-8'),cid,filesize


    # 数据获取和模板渲染
    def dbquery(self,cid,filesize):
        db=web.database(dbn='mysql',user='xmp',pw='view_hot',db='xmp_hot_view',host='127.0.0.1')
        tbl='hot_view_'+cid[0:2]
        infos=db.select(tbl, where="cid=$cid and filesize=$filesize",vars={'cid':cid,'filesize':filesize})
        res=""
        for info in infos:
            res+=r'<tr><td>'+str(info.id)+r'</td><td>'+info.cid+r'</td><td>'+str(info.filesize)+r'</td><td>'+info.ext+r'</td><td>'+str(info.duration)+r'</td><td>'+str(info.view_num)+r'</td><td>'+str(info.operate_num)+r'</td></tr>'
        
        return res
        


    # 获取保存好的json数据绘制view和高潮区间（也可以完成整套计算）
    def drawhigh(cid,filesize):
        # 获取view和high数据
        viewfile=os.path.join('/usr/local/sandai/xmp_hotview/data',cid[0:2],cid[2:4],cid+"."+filesize)  # 确定原始数据的路径
        vfb = open(viewfile)
        try:
                hot_info = vfb.read()
                jsob_body = json.loads(hot_info)
                view = jsob_body.get("hot_view")
        except Exception,e:
                s=sys.exc_info()
                print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)
        finally:
                vfb.close()

        highfile=os.path.join('/data1/xmp_hotview/highdur/',cid[0:2],cid[2:4],cid+"."+filesize)         # 确定高潮数据的路径
        hfb = open(highfile)
        try:
                hot_info = hfb.read()
                jsob_body = json.loads(hot_info)
                high = jsob_body.get("highdur")
        except Exception,e:
                s=sys.exc_info()
                print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)
        finally:
                hfb.close()

        # 图像设置
        plt.figure(figsize=(15,7))  # figsize()设置的宽高比例是是15:7，图片的尺寸会根据这个比例进行调节
        plt.ylim(min(view)-500,max(view)+500)
        plt.grid(which='both')

        # 绘制原始数据
        plt.plot(range(1,len(view)+1),view,color='y',lw=0.5,label='origin')
        plt.legend(loc='upper right')
        plt.xlabel('time (s)')
        plt.ylabel('views')

        # 当存在高潮区间的时候标注高潮区间
        if high:
            for item in high:
                plt.annotate('',xy=(item[1],1000),xytext=(item[0],1000),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
                plt.fill_betweenx([lowlimit,highlimit],item[0], item[1], linewidth=1, alpha=0.2, color='r')

        # 结果保存（能不能不保存，直接获取图像数据显示）
        '''
    despath='/data1/xmp_hotview/highpic/'
        if not os.path.exists(despath):
                os.makekdirs(despath)
        fname=os.path.join(despath,cid+'.'+str(filesize)+'.jpg')
        plt.savefig(fname,dpi = 300)
        plt.close()
    '''

if __name__=="__main__":
    print "hahw"
    pass
    #这是测试tab键
