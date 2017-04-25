#!/bin/env python
# -*- coding: utf8 -*-
'''
	fun:下载优酷首视频初版，不分类
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

if 'Windows' in platform.system():
	path='D:\\'
else:
	path=os.path.split(os.path.realpath(sys.argv[0]))[0]
	path = path +'/'
print path



# 获取sid和token
def get_sid_token(encrypt_string):
	k=pyDes.des('e5571054', pyDes.ECB, "\0\0\0\0\0\0\0\0", pad='\32', padmode=pyDes.PAD_NORMAL)
	enh=base64.decodestring(encrypt_string)
	data = k.decrypt(enh)
	data = data.split('\0')[0]
	print data
	return data

# 获取ep
def get_ep(fileid, sid, token):
	src = sid+'_'+fileid+'_'+token
	k=pyDes.des('bf09f477', pyDes.ECB, "\0\0\0\0\0\0\0\0", pad='\0', padmode=pyDes.PAD_NORMAL)
	print src
	d = k.encrypt(str(src))
	ep = base64.b64encode(d)
	return urllib.quote_plus(ep)

# 显示执行进度
def Schedule(a,b,c):
	'''
	a:已经下载的数据块
	b:数据块的大小
	c:远程文件的大小
	'''
	per = 100.0 * a * b / c
	if per > 100 :
		per = 100

	print '%.2f%%' % per

# url根据url下载文件和选择保存
def down_load(down_url, save_file):
	try:
		urllib.urlretrieve(down_url,save_file,Schedule)
		'''
		response = urllib2.urlopen(get_down_url)		
		data=response.read()
			
		f=open(filename,'wb')
		print filename
		f.write(data)
		'''
	except Exception,e:
		#traceback.print_exc()
		print 'timeout...'
	


	
if "__main__" == __name__:
	print 'OK......'
	url = 'http://v.youku.com/v_show/id_XOTM1MTEwODQ0.html'
	url = 'http://v.youku.com/v_show/id_XMTU3Njg4NTI0MA==.html'
	url = 'http://v.youku.com/v_show/id_XOTM1MTEwODQ0.html'
	pat=re.compile("id_(.*).html")
	id = pat.findall(url)[0]
	print "id:",id

	#第一步
	url_get_json = 'http://play.youku.com/play/get.json?vid='+id+'&ct=13&yktk=&uniqueid=f8b156b94a17&ran=4'
	print url_get_json
	response = urllib2.urlopen(url_get_json)
	data=response.read()
	#print data
	
	#第二步，解析json数据
	json_data=json.loads(data)
	title = json_data['data']['video']['title']
	#encrypt_string
	encrypt_string = json_data['data']['security']['encrypt_string']
	print(title,encrypt_string)  # 获取title和加密字符串
	
	#sid , token
	sid_token = get_sid_token(encrypt_string)
	sid_token = sid_token.split('_')
	sid = str(sid_token[0])
	token = str(sid_token[1])


	f=open(title+'_down_url','w')
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
				fileid = seg['fileid']
				key = str(seg['key'])
				total_milliseconds_video = str(seg['total_milliseconds_video'])
				#print fileid,',',key
				index = '%02d' % (int(fileid[8:10],16))
				
				ep = get_ep(fileid, sid, token)
				print 'ep:',ep
				get_down_url = 'http://k.youku.com/player/getFlvPath/sid/'+sid+'_'+index+'/st/flv/fileid/'+fileid+'?K='+key+'&ctype=13&ep='+ep+'&ev=1&hd=0&oip=3682970194&token='+token+'&ts='+total_milliseconds_video+'&ypp=0'
				print get_down_url
				f.write(get_down_url+'\n')
				filename = path+title+'-'+index+'.flv'
				down_load(get_down_url,filename)
			break
	f.close()
		

			
			
			
			
			

			
			
			
			
			
			
			
			
			
			