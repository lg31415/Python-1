#!/bin/env python
# -*- coding: utf8 -*-
'''
	Date:
	Author:tuling56
	Fun:模拟客户端下载优酷视频
'''

import os
import sys
import base64
import pyDes
import urllib2
import urllib
import re
import json
import traceback
import platform
import socket
import struct

reload(sys)
sys.setdefaultencoding( "utf-8" )

class youku_video_download:
	def __init__(self):
		self.title = ''
		self.segs_info=[]
		if 'Windows' in platform.system():
			self.down_path='c:\\'
		else:
			self.down_path=os.path.split(os.path.realpath(sys.argv[0]))[0]
			self.down_path = self.down_path +'/'
			self.merge_conf_file = self.down_path + 'mergelist.txt'
		print self.down_path
		
	def get_ip_address(self,ifname):
		'''获取外网IP数字形式'''
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		ip = socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
			struct.pack('256s', ifname[:15])
		)[20:24])
		ntoa = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
		return ntoa(ip)
	
	def get_sid_token(self,encrypt_string):
		'''计算关键参数sid和token'''
		k=pyDes.des('e5571054', pyDes.ECB, "\0\0\0\0\0\0\0\0", pad='\32', padmode=pyDes.PAD_NORMAL)
		enh=base64.decodestring(encrypt_string)
		data = k.decrypt(enh)
		data = data.split('\0')[0]
		print data
		return data

	def get_ep(self,fileid, sid, token):
		'''计算关键参数ep'''
		src = sid+'_'+fileid+'_'+token
		print src
		k=pyDes.des('bf09f477', pyDes.ECB, "\0\0\0\0\0\0\0\0", pad='\0', padmode=pyDes.PAD_NORMAL)
		d = k.encrypt(str(src))
		ep = base64.b64encode(d)
		return urllib.quote_plus(ep)
	
	def parse_video_info(self,play_url):
		'''解析分片视频信息'''
		pat=re.compile("id_(.*).html")
		id = pat.findall(play_url)[0]
		print id

		#第一步
		url_get_json = 'http://play.youku.com/play/get.json?vid='+id+'&ct=13&yktk=&uniqueid=f8b156b94a17&ran=4'
		print url_get_json
		response = urllib2.urlopen(url_get_json)
		data=response.read()
	
		#第二步，解析json数据
		json_data=json.loads(data)
	
		self.title = json_data['data']['video']['title']
		#self.title = self.title.replace(' ', '\\ ')
		print self.title
	
		#encrypt_string
		encrypt_string = json_data['data']['security']['encrypt_string']
	
		#sid , token
		sid_token = self.get_sid_token(encrypt_string)
		sid_token = sid_token.split('_')
		sid = str(sid_token[0])
		token = str(sid_token[1])
	
		lists = json_data['data']['stream']
		for item in lists:
			stream_type = item['stream_type']
			audio_lang = item['audio_lang']
			width = item['width']
			print stream_type,',',audio_lang,',',width
			#if stream_type=='flvhd' and audio_lang=='guoyu':
			if stream_type=='flvhd':
				segs = item['segs']
				#视频片段
				for seg in segs:
					item={}
					fileid = seg['fileid']
					key = str(seg['key'])
					total_milliseconds_video = str(seg['total_milliseconds_video'])
					size = seg['size']
					print 'size:',size
					#print fileid,',',key
					index = '%02d' % (int(fileid[8:10],16))
					
					ep = self.get_ep(fileid, sid, token)
					print 'ep:',ep
					oip = self.get_ip_address('eth0')
					get_down_url = 'http://k.youku.com/player/getFlvPath/sid/'+sid+'_'+index+'/st/flv/fileid/'+fileid+'?K='+key+'&ctype=13&ep='+ep+'&ev=1&hd=0&oip='+str(oip)+'&token='+token+'&ts='+total_milliseconds_video+'&ypp=0'
					print get_down_url
					filename = self.down_path+self.title+'-'+index+'.flv'
					item['down_url'] = get_down_url
					item['file_name'] = filename
					item['file_size'] = size
					self.segs_info.append(item)
					#down_load(get_down_url,filename)
				break

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
				urllib.urlretrieve(down_url,save_file,self.Schedule)
			except Exception,e:
				traceback.print_exc()
				print 'timeout...'
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
	
	def merge_seg_file(self):
		'''合并分段文件'''
		print u'合并分段文件......'
		if len(self.segs_info) == 1:
			return
		print 'open file :',self.merge_conf_file
		f= open(self.merge_conf_file,'w')
		for seg in self.segs_info:
			file_path = seg['file_name'].encode('utf8')
			print file_path
			line = "file '%s'\n" % (file_path)
			f.write(line)
		f.close()
		outfile_name = r'%s.flv' % (self.title)
		print outfile_name
		if os.path.exists(outfile_name):
			print u'删除文件......'
			os.remove(outfile_name)

		cmd = 'ffmpeg -safe 0 -f concat -i %s -c copy %s' % (self.merge_conf_file,outfile_name.replace(' ', '\\ '))
		print cmd
		os.system(cmd)
		
if "__main__" == __name__:
	print 'OK......'
	url = 'http://v.youku.com/v_show/id_XOTM1MTEwODQ0.html'
	#url = 'http://v.youku.com/v_show/id_XMTU3Njg4NTI0MA==.html'
	url = 'http://v.youku.com/v_show/id_XMTUxNTM2NDA4OA==.html'
	down_load = youku_video_download()

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
	
	
	
