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
			plain_text = plain_text.rstrip(last_c)
			
		return plain_text
	
t1='F48E38A98575TJTE'
s1='PFhh7bsb/uD0SjU3DfECtUDe4lmB8G5A0NTTmYoBeQcGGch8Nf5nPOtgvqGmUs32ko7MIFu89L3kD/OKGgevVySg1S5eIrj3vsN5KL3jN2rOt3nchNSdlYHhuk5dQSEU/k5wKg7LF1PpONAFKqWnnepLKS/Dpn2Pqg68IKcoigT3Cu9ZU/2aQoZ4ROEGLxjnPLcKAzOI2RkGc8VLO69DhboKxps6T9Xgs0IF1x/OoDcORE8fQ6CJQb/m7BRouxFdXeCZYSrGeMAaO6bSAlargoMcaktSzJ3Z9Z6F412PBsv0EQx5Pp2CDVKVEsQ55NtKR5lO21qP3TKR4f8OWWdwgBREZiXYhc1SpSPerIjY3HM='

p2='94DE802AE3DAEZ3E'	
s2='PFhh7bsb/uD0SjU3DfECtQCREPhp585IR0VqEgW42xk38vIoi2A1lA5iG4XPVvpaD7VgWeYbei+C0hbXgPMGVeUadR737IokHpdVdIKcl3cynSKLi3ehMndaQDpyfwX9usZpmAEf7+RSWH+lm80Kb61e/UNJ+EhBc0WXsbXWqTrDqT5f1z6rpTEnRzUCIjH/5v7C4KQ10+56E5rfvKk1/X07cZ69NDgfbw59aMek/Dyzd6IZBSr9Ac6OS4qNdE5'

p3='002556B656CE3MRE'
s3='PFhh7bsb/uD0SjU3DfECtRXVGcv8grfmwF9E4YwPqrL+bcnY60U9L8ysKEcocwvDD7VgWeYbei+C0hbXgPMGVeUadR737IokHpdVdIKcl3cynSKLi3ehMndaQDpyfwX9UMHpIMAAiiwFgSdaK56w63Yj2J+mqpiIq5aeQwsaLljDqT5f1z6rpTEnRzUCIjH/5v7C4KQ10+56E5rfvKk1/X07cZ69NDgfbw59aMek/Dyzd6IZBSr9Ac6OS4qNdE5'

if __name__ == '__main__':
	#key = '546hcmwxcnnzdm23494DE802AE3DAEZ3E'
	key='546hcmwxcnnzdm234'+p3
	aes = XMP_AES(key)
	encrypt_str=s3
	print '[encrypt_str]:', encrypt_str
	decode_str = aes.decode(encrypt_str)
	print '[decode_str]:',decode_str
	print '---------------------------------------------------'