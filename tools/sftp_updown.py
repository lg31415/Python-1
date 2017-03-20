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

	# sftp demo
	def demo(self):
		scp=paramiko.Transport(('127.0.0.1',122))

		#建立连接
		scp.connect(username='root',password='123')

		#建立一个sftp客户端对象，通过ssh transport操作远程文件
		sftp=paramiko.SFTPClient.from_transport(scp)

		#Copy a remote file (remotepath) from the SFTP server to the local host(要求两端都必须是文件，但可以修改文件名)
		sftp.get('/tmp/logrotate.log',r'D:\\xxx.log')

		#Copy a local file (localpath) to the SFTP server as remotepath(要求两端都必须是文件，但可以修改文件名)
		#sftp.put(r'E:\XMP\Record\Problems\calc_active_newinstall_overlap.sh','/tmp/overlap.sh')

		scp.close()
		sftp.close()

	# sftp上传
	def sftp_upload(self):
		pass

	# sftp下载
	def sftp_download(self):
		pass



'''
	SFTP实现文件的上传和下载
'''
class SFTP_TOOL():
	def __init__(self,host,port,username,passwd):
		# 远程执行
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(host,port,username,passwd,timeout=5)

		# 远程传输
		sf = paramiko.Transport((host,port))
		sf.connect(username = username,password = passwd)
		self.sftp = paramiko.SFTPClient.from_transport(sf)
		self.remote_sep="/"
		self.local_sep="\\"

	# 平台判定
	def judge_platform(self):
		pass


	# 判定远程文件是否是目录
	def judge_dir(self,dir):
		cmd='if [ -d {dir} ] ;then echo 1;else echo 0; fi'.format(dir=dir)
		#print cmd
		stdin,stdout,stderr = self.ssh.exec_command(cmd)
		if len(stderr.read())>0:
			print "%s wrong" %cmd
			return  -1
		res=stdout.read().strip('\n')
		if res=="1":
			return True
		else:
			return False

	# 远程创建目录
	def remote_mkdir(self,dir):
		cmd='mkdir {dir} && echo 1 ||echo 0'.format(dir=dir)
		stdin,stdout,stderr = self.ssh.exec_command(cmd)
		if len(stderr.read())>0:
			print "%s wrong" %cmd
			return  -1
		res=stdout.read().strip('\n')
		if res=="1":
			return True
		else:
			return False


	# 文件和文件夹上传
	def sftp_upload(self,local,remote):
		try:
			if os.path.isdir(local):					#判断本地参数是目录还是文件
				for root,dirs,files in os.walk(local):
					for f in files:
						localf=self.local_sep.join([root,f])
						remotep=root.replace(local,remote)
						remotep=remotep.replace(self.local_sep,self.remote_sep)
						remotef=self.remote_sep.join([remotep,f])  # 远程文件存放地址
						if not self.judge_dir(remotep):
							self.remote_mkdir(remotep)
						self.sftp.put(localf,remotef)	#上传目录中的文件
			else:
				self.sftp.put(local,remote)				#上传文件
		except Exception,e:
			print('upload exception:',e)
		self.sftp.close()
		self.ssh.close()

	# 获取远程文件列表(目录为键，名为值)
	def get_remote_list(self,dir):
		rdf_dict={}
		cmd="cd {dir} && find .  -type f".format(dir=dir)
		stdin,stdout,stderr = self.ssh.exec_command(cmd)
		for f in  stdout.readlines():
			f=f.strip("\n").strip('./')
			rd,rf=f.split(self.remote_sep)
			rdf_dict[rd]=rf
		return  rdf_dict

	# 文件和文件夹下载
	def sftp_download(self,remote,local):
		try:
			rdf=self.get_remote_list(remote)
			for rd,rf in rdf.iteritems():
				remotef=self.remote_sep([remote,rd,rf])
				localp=os.path.join(local,rd.replace(self.remote_sep,self.local_sep))
				localf=self.local_sep.join([localp,rf])  # 远程文件存放地址
				if not os.path.exists(localp):
					os.makedirs(localp)
				self.sftp.get(remotef,localf)
			else:
				self.sftp.get(remote,local)
		except Exception,e:
			print('download exception:',e)
		self.sftp.close()
		self.ssh.close()

	# 测试
	def sftp_test(self):
		print self.sftp



'''
	测试入口
'''
if __name__ == "__main__":
	# 测试
	#sdemo=SFTP_LAB()
	#sdemo.demo()
	#sys.exit()

	# 上线
	sftp_tool=SFTP_TOOL('127.0.0.1',122,'root','123')
	#sftp_tool.sftp_upload("D:\\cygwin64\\home\\yjm\\data\\subdir",'/home/yjm')
	sftp_tool.sftp_download('/usr/local/nginx/conf/vhosts','D:\\')
