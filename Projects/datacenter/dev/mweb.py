#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：
'''
import web
import os,sys,json
import matplotlib.pyplot as plt  #绘图使用

# 全局设置
urls = (
    '/([0-9a-zA-Z]{1,})[^/]*', 'BASIC',
    '/render/(.*)?','RENDER',
    '/db/(.*)?','DBO'
)

app = web.application(urls)

'''
    基本操作：
    1,Get方法参数是如何传输进去的,url匹配到的部分都被捕捉了到Get的参数中
    2.Post方法的网页的表单数据是如何传递到服务器中，然后是怎样被解析的
'''
class BASIC:
    def GET(self,name):
        print u"传递的参数是：",name
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'

    def POST(self):
        data=web.data()
        '''通过xml使用post来传递数据
        xml = etree.fromstring(data)
        content = xml.find('Content').text
        print type(content),content
        return content
        '''
        print type(data),'\n',data
        return  data



'''
    模板操作:
    1,传递的参数渲染到html模板中去，实现html操作python的功能
    2,本身自带的html模板功能太弱，建议使用JinJa2模板
'''
render = web.template.render('templetes/')

class RENDER:
    def GET(self,paraso):
        print u"传递的参数是:",paraso
        parasi = web.input(name=None,age=None)
        oview=self.getview(parasi.name,parasi.age)
        res= render.datacenter_v2(oview)
        #res=render.index1(parasi.name,parasi.age)
        return res

    def getview(self,cid,filesize):
        #readfile=os.path.join('/usr/local/sandai/xmp_hotview/data',line[0:2],line[2:4],line)
        readfile='./templetes/data/origin.json'
        print readfile
        rfb = open(readfile)
        try:
            hot_info = rfb.read()
            jsob_body = json.loads(hot_info)
            view = jsob_body.get("hot_view")
        except Exception,e:
            s=sys.exc_info()
            print "\033[1;31mError: '%s' happened on line %d\033[0m" % (s[1],s[2].tb_lineno)
        finally:
            rfb.close()
        return  view



'''
    数据库操作:
    1,利用模板组装数据
'''
class DBO:
    def GET(self,paraso):
        print u"传递所有参数:", paraso
        # 参数解析
        web.ctx.status="200"
        paras=web.input(id=0,name="wang")
        id=paras["id"]
        name=paras["name"]
        print u"传递解析得到的id和name:",id,name

        # 数据库查询
        db=web.database(dbn='mysql',user='root',pw='root',db='study',host='127.0.0.1')
        users=db.select('test', where="id>$od and name!=$name",vars={'od':id,'name':name})
        info=""
        for user in users:
            print user.id,user.name,user.score
            info+=r'<tr><td>'+str(user.id)+r'</td><td>'+user.name+r'</td><td>'+str(user.score)+r'</td></tr>'
        print info
        return render.dbquery(['hahhah','wang'],info)

        # 高级查询
        #results = db.query("SELECT * FROM test JOIN users WHERE entries.author_id = users.id")

        # 增删改的操作
        #db.insert('test',id='222222',name='wangwangwang',score='100')
        #db.update('test',where='id>$id',vars={'id':2},name='SHE',score=0)
        #db.delete('test',where='id=$id',vars={'id':1})

    def POST(self,paras):
        web.ctx.status="400"
        #data=web.data() # 也可以使用这种方法
        paras=web.input(id=None,name=None)
        id=paras["id"]
        name=paras["name"]
        print id,name
        return u"哈哈哈哈,这是post的返回结果：".encode('utf-8'),id,name

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
        lowlimit=min(view)-500      #y轴下限
        highlimit=max(view)+500     #y轴上限
        plt.ylim(lowlimit,highlimit)
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
        despath='D:\\hot_pic1'
        if not os.path.exists(despath):
            os.makekdirs(despath)
        fname=os.path.join(despath,cid+'.'+str(filesize)+'.jpg')
        plt.savefig(fname,dpi = 300)
        plt.close()



# 程序入口
if __name__ == "__main__":
    app.run()
