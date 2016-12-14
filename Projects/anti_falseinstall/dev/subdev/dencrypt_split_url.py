#!/usr/bin/env python
#coding: utf8

#add by luochuan@xunlei.com 2016-09-21 Wed
from Crypto.Cipher import AES
import base64

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
		if (count % length) != 0:
			fill = length - (count % length)
			#print fill
			text = text + (chr(fill) * fill)

		self.ciphertext = cryptor.encrypt(text)
		return base64.b64encode(self.ciphertext)

	def decode(self, text):
		cryptor = AES.new(self.key, self.mode, self.key)
		plain_text = cryptor.decrypt(base64.b64decode(text))
		last_c = plain_text[-1]
		if ord(last_c) <= 16:
			#print "→[去白%s]%d" %(last_c,plain_text.count(last_c))
			plain_text = plain_text.rstrip(last_c)
			
		return plain_text

def urlsplit(encrypt_url):
	data_set={'install':'','installtype':'','newinstall':'','version':'','package_name':'','lastinstallsource':''}
	url=encrypt_url.strip().split("&")
	for i in range(0,len(url)):
		if len(url[i])>0 and url[i].find('=')!=-1:
			key,value = url[i].split("=")
			if key in data_set :
				data_set[key] = value

	return "\t".join([data_set["installtype"],data_set['newinstall'],data_set['version'],data_set['package_name'],data_set['lastinstallsource']])


def test():
	key='546hcmwxcnnzdm234'
	aes = XMP_AES(key)
	encrypt_str ='OKGCCnYU3gr7t//WCOiE1VF36AzKyh2wX2wD8C7aION+J4/1jlswymNgGFu7N+mc8xDmf+u3OUCMABAK5Rq7glJPIPNeQVWRZn3UUjmdf0UUA0lnoGVOFM1uSeoUsA4w' #aes.encode(origin_str)
	print '[key]:',key
	#print '[origin_str]:',origin_str
	print '[encrypt_str]:',len(encrypt_str),'\n',encrypt_str
	decode_str = aes.decode(encrypt_str)
	print '[decode_str]:',len(decode_str),'\n',decode_str
	print '---------------------------------------------------'



if __name__ == '__main__':
	key='546hcmwxcnnzdm234'
	aes = XMP_AES(key)
	with open('anti_install_1_20160927') as f:
		for line in f:
			peerid,encrypt_url=line.strip().split('\t')
			encrypt_url='+'.join(encrypt_url.split())
			try:
				decode_str=aes.decode(encrypt_url)
				#print decode_str
				print peerid+"\t"+urlsplit(decode_str)
			except Exception,e:
				#print '\033[31m%s\033[0m' %str(e)
				#print len(encrypt_url),'\n',encrypt_url
				continue