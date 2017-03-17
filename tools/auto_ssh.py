#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:ssh自动链接和远程执行命令
	Ref:http://mp.weixin.qq.com/s/2P2IyrF8aCsUnsXsaNWuZA
	State：
	Date:2017/3/16
	Author:tuling56
'''
import re, os, sys
import hues
import paramiko
#paramiko.util.log_to_file('/tmp/sshout')

reload(sys)
sys.setdefaultencoding('utf-8')

'''
	连接和执行远程命令
'''
def ssh_connect(ip,username,passwd,cmd):
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,122,username,passwd,timeout=5)
		stdin,stdout,stderr = ssh.exec_command(cmd)
#		stdin.write("Y")   #简单交互，输入 ‘Y’
		print stdout.read()
		for x in  stdout.readlines():
			print x.strip("n")
		print '%stOKn'%(ip)
		ssh.close()
	except :
		print '%stErrorn'%(ip)


if __name__ == "__main__":
	ssh_connect("127.0.0.1","root","123","hostname;ifconfig")

