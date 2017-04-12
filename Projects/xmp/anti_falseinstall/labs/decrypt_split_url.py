#!/usr/bin/env python
#coding: utf8

#add by luochuan@xunlei.com 2016-09-21 Wed
from Crypto.Cipher import AES
import base64
import sys
import re


'''
	解密工具
'''
class XMP_AES():
	def __init__(self, key, mode = AES.MODE_ECB, keyLength = 16):
		if len(key) == keyLength:
			self.key = key
		elif len(key) > keyLength:
			self.key = key[0:keyLength]
		else:
			self.key = key + ('\0' * (keyLength - len(key)))
			
		self.mode = mode

	def encode(self, text):
		cryptor = AES.new(self.key, self.mode, self.key)
		count = len(text)
		length = 16
		fill = length - (count % length)
		#print fill
		text = text + (chr(fill) * fill)

		self.ciphertext = cryptor.encrypt(text)
		return base64.b64encode(self.ciphertext)

	
	def decode(self, text):
		cryptor = AES.new(self.key, self.mode, self.key)
		try:
			b64dec=base64.b64decode(text)
		except Exception,e:
			print "\033[1;31mbase64 decode error:\033[0m",str(e)
			print "[to base64 decode]:",text
			return ""
		
		try:
			plain_text = cryptor.decrypt(b64dec)
		except Exception,e:
			print "\033[1;31m des decode error:\033[0m",str(e)
			print "[to aes decode]:",b64dec
			return ""

		last_c = plain_text[-1]
		if ord(last_c) <= 16:
			#print "→[去白%s]%d" %(last_c,plain_text.count(last_c))
			plain_text = plain_text.rstrip(last_c)
			
		return plain_text

'''
	url分割
'''
def urlsplit(encrypt_url):
	data_set={'install':'','installtype':'','newinstall':'','version':'','package_name':'','lastinstallsource':''}
	url=encrypt_url.strip().split("&")
	for i in range(0,len(url)):
		if len(url[i])>0 and url[i].find('=')!=-1:
			key,value = url[i].split("=")
			if key in data_set :
				data_set[key] = value

	return "\t".join([data_set["installtype"],data_set['newinstall'],data_set['version'],data_set['package_name'],data_set['lastinstallsource']])


'''
	测试
'''
def test():
	key='546hcmwxcnnzdm234'
	aes = XMP_AES(key)
	encrypt_str ='PFhh7bsb/uD0SjU3DfECtRXVGcv8grfmwF9E4YwPqrJUlvDLMfyoKuGijGuOKMfVD7VgWeYbei+C0hbXgPMGVeUadR737IokHpdVdIKcl3cynSKLi3ehMndaQDpyfwX9u6VfG+IzsviS+hLGUW7mzn2UxL7uqFvFPseEv5CV2OjDqT5f1z6rpTEnRzUCIjH/5v7C4KQ10+56E5rfvKk1/dyVQV4pLnN2k+6H1+kdB3ezd6IZBSr9Ac6OS4qNdE5' #aes.encode(origin_str)
	print '[key]:',key
	#print '[origin_str]:',origin_str
	print '[encrypt_str]:',len(encrypt_str),'\n',encrypt_str
	decode_str = aes.decode(encrypt_str)
	print '[decode_str]:',len(decode_str),'\n',decode_str
	print '---------------------------------------------------'


##### 程序主入口
if __name__ == '__main__':
	input=sys.argv[1]
	date=re.search('\d{8}$',input).group()
	
	output=sys.argv[2]
	fout=open(output,'w')
	
	fouterror=open('decrypt_error','w')
	
	print '[date]:',date
	print '[input]:',input
	print '[output]:',output
	
	key='546hcmwxcnnzdm234'
	aes = XMP_AES(key)
	with open(input,'r') as f:
		for line in f:
			try:
				peerid,encrypt_url=line.strip().strip('\n').split('\t')
				encrypt_url='+'.join(encrypt_url.split())
				print '----------------------------------------------'
				print '[encrypt_url]:',encrypt_url
				decode_str=aes.decode(encrypt_url)
				if  decode_str:
					print "[decode_str]:",decode_str
					info=date+"\t"+peerid+"\t"+urlsplit(decode_str)+"\tdecrypt\n"
					fout.write(info)
			except Exception,e:
				print '\033[31m%s\033[0m' %str(e)
				#fouterror.write(str(len(encrypt_url))+" | "+str(len(line))+"\r\n")
				fouterror.write(line)
				continue
	fout.close()
	fouterror.close()
