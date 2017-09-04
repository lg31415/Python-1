#!/usr/bin/env python
#coding: utf8
#add by luochuan@xunlei.com 2016-09-21 Wed
__author__ = 'yjm'
'''
  功能注释：aes加解密算法
'''
from Crypto.Cipher import AES
import base64

class XMP_AES():
    #key的使用法则
    def __init__(self, key, mode = AES.MODE_ECB, keyLength = 16):
        if len(key) == keyLength:
            self.key = key
        elif len(key) > keyLength:
            self.key = key[0:keyLength]
        else:
            self.key = key + ('\0' * (keyLength - len(key)))  #密钥长度右补充0
            
        self.mode = mode

    # 先aes加密，再base64编码
    def encode(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        count = len(text)
        length = 16
        if (count % length) != 0:  #如果被编码的字符不到16位，则填充法则如下
            fill = length - (count % length)
            #print fill
            text = text + (chr(fill) * fill)

        self.ciphertext = cryptor.encrypt(text)
        return base64.b64encode(self.ciphertext)


    # 先base64解码，再aes解密
    def decode(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        dbase64=base64.b64decode(text)
        if len(dbase64)%16!=0:
            print '[len(dbase64)]:',len(dbase64)
            dbase64=dbase64+chr(16-len(dbase64)%16)*(16-len(dbase64)%16)  #填充位
            #dbase64=dbase64[:(len(dbase64)-len(dbase64)%16)]
            print '[dbase64]:',dbase64
        plain_text = cryptor.decrypt(dbase64)  #此处解密的时候出现问题，提示解密的字符串不是16的整数倍
        last_c = plain_text[-1]
        if ord(last_c) <= 16:
            plain_text = plain_text.rstrip(last_c)
            
        return plain_text




############### 功能测试区
t1='F48E38A98575TJTE'
s1='PFhh7bsb/uD0SjU3DfECtUDe4lmB8G5A0NTTmYoBeQcGGch8Nf5nPOtgvqGmUs32ko7MIFu89L3kD/OKGgevVySg1S5eIrj3vsN5KL3jN2rOt3nchNSdlYHhuk5dQSEU/k5wKg7LF1PpONAFKqWnnepLKS/Dpn2Pqg68IKcoigT3Cu9ZU/2aQoZ4ROEGLxjnPLcKAzOI2RkGc8VLO69DhboKxps6T9Xgs0IF1x/OoDcORE8fQ6CJQb/m7BRouxFdXeCZYSrGeMAaO6bSAlargoMcaktSzJ3Z9Z6F412PBsv0EQx5Pp2CDVKVEsQ55NtKR5lO21qP3TKR4f8OWWdwgBREZiXYhc1SpSPerIjY3HM='

p2='1C1B0D1F912471OE'    
s2='OKGCCnYU3gr7t//WCOiE1VF36AzKyh2wX2wD8C7aION J4/1jlswymNgGFu7N mc8xDmf u3OUCMABAK5Rq7ggSWslas25cRkYewCDhbL54MIWD0Eo7dhCyU/mzV7LuRG44W6z4drBK5n ggcC2tEQ=='

p3=''
s3="hs887a4on6PkWrmIK5ObDmw5dHX1hkdNnxAr/so+tfgn9N7lt2Twcp5F7U+fi1hako7MIFu89L3kD/OKGgevVySg1S5eIrj3vsN5KL3jN2rOt3nchNSdlYHhuk5dQSEUfaeeEuEZBWXMmQzGkctupHxrzLfXvPk4xyekSaSfPL73Cu9ZU/2aQoZ4ROEGLxjnVu095LaGSXVsA84ZS+U517oKxps6T9Xgs0IF1x/OoDcovft5KVhhR2XOk3dO2CGq/t0i+7I7ybsOSEVoXE9+1oMcaktSzJ3Z9Z6F412PBsveEeJxLz6qaEnLuzNpolA98RoCo9GPRXkCMnHzqwsHUgLLE86vP9VkvjtbSiI3AUM="

p4=''
s4='hs887a4on6PkWrmIK5ObDmw5dHX1hkdNnxAr/so+tfgn9N7lt2Twcp5F7U+fi1hako7MIFu89L3kD/OKGgevVySg1S5eIrj3vsN5KL3jN2rOt3nchNSdlYHhuk5dQSEUfaeeEuEZBWXMmQzGkctupOF9j5L/L8qvhhINtTJDm033Cu9ZU/2aQoZ4ROEGLxjnVu095LaGSXVsA84ZS+U517oKxps6T9Xgs0IF1x/OoDcovft5KVhhR2XOk3dO2CGqj9aDega1HGnMv/ezzCpbkYMcaktSzJ3Z9Z6F412PBsveEeJxLz6qaEnLuzNpolA98RoCo9GPRXkCMnHzqwsHUgLLE86vP9VkvjtbSiI3AUM='

if __name__ == '__main__':
    key='546hcmwxcnnzdm234'+p4
    aes = XMP_AES(key)
    encrypt_str=s4
    print '[len(encrypt_str)]:',len(encrypt_str)
    print '[encrypt_str]:', len(encrypt_str),'\n',encrypt_str
    decode_str = aes.decode(encrypt_str)
    print '[decode_str]:',decode_str
    print '---------------------------------------------------'