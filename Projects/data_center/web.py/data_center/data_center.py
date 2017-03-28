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


# 全局设置
urls = (
	'/','Handler'
)

app = web.application(urls,globals()) #此处的global必不可少

# 测试类
class TEST(object):
	def GET(self):
		render = web.template.render('./templetes/')
		res=render.index()
		return res

'''
    模板操作:
    1,传递的参数渲染到html模板中去，实现html操作python的功能
'''
class Handler(object):
	def __init__(self):
		self.render = web.template.render('./templetes/')
		self.res="这是欢迎页面"

	# 处理Get请求
	def GET(self):
		web.ctx.status = "200"

		# 参数解析
		try:
			params = web.input(cid =None, filesize=0)
			cid = params["cid"]
			filesize = params["filesize"]
		except Exception,e:
			print u"参数解析错误：",str(e)

		# 根据url调用相应的类
		try:
			# 数据库请求（然后将查询结果数据进行网页展示）
			qr=self.GetDB(cid,filesize)
			self.res=self.render.dbquery(qr)
			
			# json数据请求(然后将json数据网页可视化）
			#oview=self.GetJson(cid,filesize)
			#self.res=self.render.drawjson(oview)
		except ValueError:
			traceback.print_exc()
			print "server proc error!"
		
		return  self.res
		
	# 处理post请求
	def POST(self):
		web.ctx.status="400"
		#data=web.data() # 也可以使用这种方法
		paras=web.input(cid=None,filesize=232323)
		cid=paras["cid"]
		filesize=paras["filesize"]
		qr=self.GetDB(cid,filesize)
		res=self.render.dbquery(qr)
		return res #"post is",cid,filesize

	# 数据库请求
	def GetDB(self,cid,filesize):
		db=web.database(dbn='mysql',user='root',pw='root',db='pgv_stat_yingyin',host='127.0.0.1')
		infos=db.select('hot_view_00', where="cid=$cid or filesize=$filesize",vars={'cid':cid,'filesize':filesize})
		res=""
		for info in infos:
			res+=r'<tr><td>'+str(info.id)+r'</td><td>'+info.cid+r'</td><td>'+str(info.filesize)+r'</td><td>'+info.ext+r'</td><td>'+str(info.duration)+r'</td><td>'+str(info.view_num)+r'</td><td>'+str(info.operate_num)+r'</td></tr>'

		return res
		
	# json数据请求（本地）
	def GetJson(self,cid,filesize):
		#readfile=os.path.join('/usr/local/sandai/xmp_hotview/data',line[0:2],line[2:4],line)
		readfile=r'./templetes/data/hotview_short.json'
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

	# matplotlib输出绘制图像（matplotlib绘制并将结果保存成图片）
	def matplotDrawRes(self):
		# 获取图1数据
		viewfile='./templetes/data/hotview_long.json'  # 确定原始数据的路径
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

		# 获取图2数据
		highfile='./templetes/data/highdur.json'         # 确定高潮数据的路径
		hfb = open(highfile)
		try:
				hot_info = hfb.read()
				jsob_body = json.loads(hot_info)
				high = jsob_body.get("highdur")
				high= [x.split('_') for x in high]
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

		# 矩形标注范围之间的区间high=[[23,45],[60,89]]
		for item in high:
			plt.annotate('',xy=(item[1],1000),xytext=(item[0],1000),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
			plt.fill_betweenx([10,3000],int(item[0]), int(item[1]), linewidth=1, alpha=0.2, color='r')

		# 图像结果保存(如何将结果无缝输出给展示对象就方便很多了)
		despath='./res'
		if not os.path.exists(despath):
			os.makedirs(despath)
		plt.savefig(os.path.join(despath,'res.jpg'),dpi = 300)
		plt.close()



'''
	程序单独运行或者作为uwsgi的入口
'''
if __name__ == "__main__":
	app.run()
else:
	application = app.wsgifunc()


'''
if __name__ == "__main__":
	mhand=Handler()
	mhand.matplotDrawRes()
'''