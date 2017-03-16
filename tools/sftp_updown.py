#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:Python实现sftp的上传和下载文件
	Ref:
	State：
	Date:2017/3/16
	Author:tuling56
'''
import re, os, sys
import hues
import paramiko

reload(sys)
sys.setdefaultencoding('utf-8')


'''
	SFTP实现文件的上传和下载Lab
	未解决目录上传和下载的问题
'''
class SFTP_LAB():
	def __init__(self):
		pass
	def demo(self):
		scp=paramiko.Transport(('192.168.0.102',22))
		#建立连接
		scp.connect(username='root',password='361way')
		#建立一个sftp客户端对象，通过ssh transport操作远程文件
		sftp=paramiko.SFTPClient.from_transport(scp)
		#Copy a remote file (remotepath) from the SFTP server to the local host
		sftp.get('/root/testfile','/tmp/361way')
		#Copy a local file (localpath) to the SFTP server as remotepath
		sftp.put('/root/crash-6.1.6.tar.gz','/tmp/crash-6.1.6.tar.gz')
		scp.close()
		sftp.close()
	def sftp_upload(self):
		pass
	def sftp_download(self):
		pass



'''
	SFTP实现文件的上传和下载
'''
class SFTP_TOOL():
	def __init__(self,host,port,username,passwd):
		sf = paramiko.Transport((host,port))
		sf.connect(username = username,password = passwd)
		self.sftp = paramiko.SFTPClient.from_transport(sf)
		self.remote_sep="/"
		self.local_sep="\\"

	# 平台判定
	def judge_platform(self):
		pass

	# 文件和文件夹上传
	def sftp_upload(self,local,remote):
		try:
			if os.path.isdir(local):				#判断本地参数是目录还是文件
				for f in os.listdir(local):			#遍历本地目录
					self.sftp.put(os.path.join(local+f),os.path.join(remote+f))#上传目录中的文件
			else:
				self.sftp.put(local,remote)			#上传文件
		except Exception,e:
			print('upload exception:',e)
		self.sftp.close()

	# 文件和文件夹下载
	def sftp_download(self,remote,local):
		try:
			if os.path.isdir(local):
				for f in self.sftp.listdir(remote):  # 此处列出了远程的所有的目录和文件
					self.sftp.get(self.remote_sep.join(remote+f),self.local_sep.join(local+f))
			else:
				self.sftp.get(remote,local)
		except Exception,e:
			print('download exception:',e)
		self.sftp.close()

	# 测试
	def sftp_test(self):
		print self.sftp

if __name__ == "__main__":
	sftp_tool=SFTP_TOOL('127.0.0.1',122,'root','123')
	#sftp_tool.sftp_test()
	sftp_tool.sftp_download('/usr/local/nginx/conf/vhosts','D:\\')
