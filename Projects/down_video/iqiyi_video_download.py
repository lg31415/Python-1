#!/bin/env python
# -*- coding: utf8 -*-
'''
	Date:
	Author:tuling56
	Fun:模拟客户端下载iqiyi视频
'''

import os
import sys
import base64
import pyDes
import urllib
import urllib2
import re
import json
import traceback
import platform
import socket
import struct
import time
import hashlib
import random

reload(sys)
sys.setdefaultencoding( "utf-8" )

class iqiyi_video_download:
	def __init__(self):
		self.video_info = {}
		self.segs_info=[]
		# 下载路径设置
		if 'Windows' in platform.system():
			self.down_path='d:\\'
		else:
			self.down_path=os.path.split(os.path.realpath(sys.argv[0]))[0]
			self.down_path = self.down_path +'/'
			self.merge_conf_file = self.down_path + 'mergelist.txt'
		print self.down_path

		# 代理设置
		self.proxy={'http':'http://61.135.217.12:80'}
		self.proxy = None
		if self.proxy:
			proxy = urllib2.ProxyHandler(self.proxy)
			#opener = urllib2.build_opener(proxy, urllib2.HTTPHandler(debuglevel=1))
			opener = urllib2.build_opener(proxy)
			urllib2.install_opener(opener)
	
	def get_macid(self):
		'''获取macid,此值是通过mac地址经过算法变换而来,对同一设备不变'''
		macid=''
		chars = 'abcdefghijklnmopqrstuvwxyz0123456789'
		size = len(chars)
		for i in range(32):
			macid += list(chars)[random.randint(0,size-1)]
		return macid
		#return "acwh4tcvo7z7vemcxi7ipgxcr5t6iw7i"
		
	def get_vf(self, url_params):
		'''计算关键参数vf'''
		sufix=''
		for j in range(8):
			for k in range(4):
				v4 = 13 * (66 * k + 27 * j) % 35
				if ( v4 >= 10 ):
					v8 = v4 + 88
				else:
					v8 = v4 + 49
					#src[0]=v8
				print chr(v8),' ',
				sufix += chr(v8)
		print ''
		url_params += sufix
		m = hashlib.md5()
		print url_params
		m.update(url_params)
		vf = m.hexdigest() 
		print vf
		return vf
		
	def parse_video_info(self,play_url):
		'''解析分片视频信息'''
		print play_url
		pat=re.compile("v_(.*).html")
		id = pat.findall(play_url)[0]
		print id

		#第一步
		if self.proxy:
			header = { 'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
			req = urllib2.Request(play_url,headers=header)
			response = urllib2.urlopen(req)
			#response = urllib.urlopen(play_url,proxies=self.proxy)
		else:
			response = urllib2.urlopen(play_url)
		
		content=response.read()
		
		#解析影片名
		tvName = re.findall("tvName:\"(.*)\",",content)
		if 'Windows' in platform.system():
			tvName = tvName[0].encode('gb2312')
		else:
			tvName = tvName[0].encode('utf8')
		print tvName
		self.video_info['title'] = tvName
					
		#解析tvid
		tvid = re.findall("param\['tvid'\]\s+=\s+\"(.*)\"",content)
		tvid = tvid[0]		
		print tvid
		if not tvid.isdigit():
			print u'tvid解析失败！'
			return False
		self.video_info['tvid'] = tvid
		
		#解析vid
		vid = re.findall("param\['vid'\]\s+=\s+\"(.*)\"",content)
		vid = vid[0]		
		print vid
		if len(vid) != 32:
			print u'vid解析失败！'
			return False
		self.video_info['vid'] = vid
		
		#组装获取下载链接的url
		tm = time.time()
		tm = int(tm)*1000
		host = 'http://cache.video.qiyi.com'
		src='/vps?tvid='+tvid+'&vid='+vid+'&v=0&qypid='+tvid+'_12&src=01012001010000000000&t='+str(tm)+'&k_tag=1&k_uid='+self.get_macid()+'&rs=1'
		print src
		vf = self.get_vf(src)
		req_url = host + src + '&vf=' + vf
		print req_url
		
		
		#获取视频下载链接
		if self.proxy:
			header = { 'User-Agent' : "QY-Player-Windows/2.0.106",
						'qyid':self.get_macid(),
						'qypid':tvid+"_12",
						'qyplatform':"1-2"}
			req = urllib2.Request(req_url,headers=header)
			response = urllib2.urlopen(req)
			#response = urllib.urlopen(req_url,proxies=self.proxy)
		else:
			response = urllib2.urlopen(req_url)
		
		data=response.read()
		json_data=json.loads(data)
		if not json_data or json_data['code']=='A00001':
			print u'获取下载链接信息失败'
			return False
		
		url_prefix = json_data['data']['vp']['du']
		print 'url_prefix:',url_prefix
		
		lists = json_data['data']['vp']['tkl']
		if len(lists) == 0:
			print u'获取下载链接信息失败'
			return False
			
		#获取分段视频下载链接
		for list in lists:
			vs_array = list['vs']
			for info in vs_array:
				scrsz = info['scrsz']
				duration = info['duration']
				print 'scrsz:',scrsz
				print 'duration:',duration
				
				fs_array = info['fs']
				
				for seg_info in fs_array:
					item={}
					#此url还不是真正的下载链接，还需要再请求一次才能获取下载地址
					url = seg_info['l']				
					url = url_prefix+url
					
					if self.proxy:
						header = { 'User-Agent' : "QY-Player-Windows/2.0.106"}
						req = urllib2.Request(url,headers=header)
						response = urllib2.urlopen(req)
					else:
						response = urllib2.urlopen(url)
					if response.code != 200:
						print u'获取下载地址失败'
						return False
					json_data=json.loads(response.read())
					down_url = json_data['l']
					
					#分段序号
					idx = re.findall('&qd_index=(\d+)&', url)
					idx = int(idx[0])
					item['idx']=idx
					
					filename = self.down_path+self.video_info['title']+'-'+str(idx)+'.flv'
					item['down_url'] = down_url
					item['file_name'] = filename
					item['file_size'] = seg_info['b']
					self.segs_info.append(item)		
				break
		return 	True	

	def Schedule(self,a,b,c):
		'''
		a:已经下载的数据块
		b:数据块的大小
		c:远程文件的大小
		'''
		per = 100.0 * a * b / c
		if per > 100 :
			per = 100
		print '%.2f%%' % per
		
	def begin_down_load(self):
		'''开始下载文件'''
		for seg in self.segs_info:
			down_url = seg['down_url']
			save_file = seg['file_name']
			try:
				print u'正在下载:',save_file
				if self.proxy:
					header = { 'User-Agent' : "IKUACC/8.1.0.5030"}
					req = urllib2.Request(down_url,headers=header)
					data = urllib2.urlopen(req)							
					f = open(save_file,'wb')
					f.write(data.read())
					f.close()
				else:
					urllib.urlretrieve(down_url,save_file,self.Schedule)
			except Exception,e:
				traceback.print_exc()
				return False
		return True
		
	def check_seg_file(self):
		'''检查文件是否下载成功'''
		print u'检查文件是否下载成功......'
		for seg in self.segs_info:
			file_path = seg['file_name']
			file_size = seg['file_size']
			if int(os.path.getsize(file_path)) != int(file_size):
				return False
		return True

	def delete_seg_file(self):
		'''删除分段文件'''
		print u'删除分段文件......'
		for seg in self.segs_info:
			file_path = seg['file_name']
			if os.path.exists(file_path):
				print u'正在删除文件:%s......'%(file_path)
				os.remove(file_path)

	def merge_seg_file(self):
		'''合并分段文件'''
		print u'合并分段文件......'
		if len(self.segs_info) == 1:
			print u'无需合并!'
			return
			
		print 'open file :',self.merge_conf_file
		f= open(self.merge_conf_file,'w')
		for seg in self.segs_info:
			file_path = seg['file_name'].encode('utf8')
			print file_path
			line = "file '%s'\n" % (file_path)
			f.write(line)
		f.close()
		outfile_name = r'%s.flv' % (self.video_info['title'])
		print outfile_name
		if os.path.exists(outfile_name):
			print u'删除文件......'
			os.remove(outfile_name)

		cmd = 'ffmpeg -safe 0 -f concat -i %s -c copy %s' % (self.merge_conf_file,outfile_name.replace(' ', '\\ '))
		print cmd
		os.system(cmd)
		
		#删除分段文件
		self.delete_seg_file()

# 程序执行主体
if "__main__" == __name__:
	print 'OK......'
	#url = 'http://www.iqiyi.com/v_19rrl9x1h4.html'
	#url='http://www.iqiyi.com/a_19rrhahcy1.html'
	url='http://www.iqiyi.com/v_19rrlmbbl4.html'
	down_load = iqiyi_video_download()

	if not down_load.parse_video_info(url):
		print u'获取视频下载地址异常!'
		exit()

	if not down_load.begin_down_load():
		print u'下载出现异常!'
		exit()
		
	if not down_load.check_seg_file():	
		print u'下载失败!'
		exit()
	
	print u'文件下载成功!'
	
	if 'Linux' in platform.system():
		down_load.merge_seg_file()
	
	
	
