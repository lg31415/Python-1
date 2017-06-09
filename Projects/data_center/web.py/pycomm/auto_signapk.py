#!/usr/bin/env python
# coding: utf-8

import os
import file_info
#sys.path.append("/usr/local/xvr/vod/pycomm/")
from base_conf import xvr_sign_conf 

apktool = xvr_sign_conf.apktool
javatool = xvr_sign_conf.javatool
jar_file = xvr_sign_conf.jar
pem_file = xvr_sign_conf.pem
pk8_file = xvr_sign_conf.pk8

oculus_root_path = xvr_sign_conf.oculus_root_path
package_root_path = xvr_sign_conf.package_root_path

#data_root_path = xvr_sign_conf.file_root_path
#data_root_path = '/usr/local/xvr/data/sign'
	
def del_nouse(path):
	cmd = 'rm %s -rf' %(path)
	if os.system(cmd) != 0:
		print "failed to run cmd=%s" %cmd
		return False
		
	return True
	
def signapk(deviceid, apk_file, oculussig_file = ''):
	oculussig = oculussig_file
	device_dir = '%s/%s/%s' %(package_root_path, deviceid[0:2], deviceid)
	print 'device_dir:', device_dir
	if not oculussig:
		oculussig = '%s/%s/%s/oculussig_%s' %(oculus_root_path, deviceid[0:2], deviceid, deviceid)
		
	print 'oculussig:', oculussig
	if not file_info.exists_path(oculussig):
		return False, None
	
	if not file_info.exists_path(device_dir):
		cmd = 'mkdir -p %s' %(device_dir)
		print cmd
		if os.system(cmd) != 0:
			print "failed to run cmd=%s" %cmd
			return False, None
			
	apk_name = file_info.get_prefix(apk_file)
	decocd_apk_path = '%s/%s' %(device_dir, apk_name)
	try:
		apk_file_name = file_info.get_filename(apk_file)
		#copy apk
		#cmd = 'cp %s %s' %(apk_file, device_dir)
		#print cmd
		#if os.system(cmd) != 0:
			#print "failed to run cmd=%s" %cmd
			#a = int('make Exception')
		
		#decode apk
		if not del_nouse(decocd_apk_path):
			a = int('make Exception')
		cmd = '%s d %s -o %s' %(apktool, apk_file, decocd_apk_path)
		print cmd
		if os.system(cmd) != 0:
			print "failed to run cmd=%s" %cmd
			a = int('make Exception')
			
		#copy oculussig_file
		cmd = 'cp %s %s/assets' %(oculussig, decocd_apk_path)
		print cmd
		if os.system(cmd) != 0:
			print "failed to run cmd=%s" %cmd
			a = int('make Exception')
			
		#encode apk
		cmd = '%s b %s' %(apktool, decocd_apk_path)
		print cmd
		if os.system(cmd) != 0:
			print "failed to run cmd=%s" %cmd
			a = int('make Exception')
		
		#sign
		new_apk_file = '%s/dist/%s' %(decocd_apk_path, apk_file_name)
		result_file = '%s/%s_%s.apk' %(device_dir, apk_name, deviceid)
		cmd = '%s -jar %s %s %s %s %s' %(javatool, jar_file, pem_file, pk8_file, new_apk_file, result_file)
		print cmd
		if os.system(cmd) != 0:
			print "failed to run cmd=%s" %cmd
			a = int('make Exception')
			
		del_nouse(decocd_apk_path)
		if file_info.exists_path(result_file):
			return True, result_file
		
		return False, None
		
	except Exception,e:
		print "%s:%s" %(Exception,e)
		del_nouse(decocd_apk_path)
		return False, None
		
if __name__ == '__main__':	
	apk = '/home/luochuan/test/python/check/test_luochuan.apk'
	signapk('05157df50a16cf1f', apk)
	ret, path = signapk('05157df50a16cf1f', apk, '/home/luochuan/test/sign/oculussig_05157df50a16cf1f')
	print ret
	print path

	
