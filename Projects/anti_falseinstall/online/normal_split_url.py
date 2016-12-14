#!/usr/bin/env python
# -*-coding:utf8-*-
__author='yjm'

import re
import sys

input=sys.argv[1]
date=re.search('\d{8}$',input).group()
output=sys.argv[2]

print '[date]:',date
print '[input]:',input
print '[output]:',output

fout=open(output,'w')
header = "/cgi-bin/cgi_install.fcg"

with open(input,'r') as f:
	for line in f:
		try:
			data_set={"install":"","peerid":"","installtype":"","newinstall":"","version":"","package_name":"","lastinstallsource":""}
			line=line.strip('\n')
			url = line[line.find(header)+len(header)+1:]
			ret = url.split("&")
			for i in range(0,len(ret)):
				if len(ret[i])>0 and ret[i].find('=')!=-1:
					key,value = ret[i].split("=")
					if key in data_set :
						data_set[key] = value
			if data_set["install"]=='2606':
				info=date+"\t"+"\t".join([data_set["peerid"],data_set["installtype"],data_set["newinstall"],data_set["version"],data_set["package_name"],data_set["lastinstallsource"]])
				info=info+'\tnormal\n'
				fout.write(info)
				print info
			else:
				print data_set["install"]
		except:
			t,value,traceback = sys.exc_info()
			print t,value
			continue
		finally:
			#print "[NOW:]",line
			pass
	fout.close()
