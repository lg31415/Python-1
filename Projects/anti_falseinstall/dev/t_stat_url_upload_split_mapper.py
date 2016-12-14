#!/usr/bin/env python

import sys,re,os,re
header = "/cgi-bin/cgi_install.fcg"
for line in sys.stdin:
        try:
                url,fip,ftime = line.rstrip().split('\t')
                data_set={"install":"","channel":"","peerid":"","newinstall":"","firstinstallsource":"","firstinstaltime":"","installtime":"","installtype":"","lastuninstalltime":"","firstinstallversion":"","version":"","package_name":"","lastinstallsource":"","fatherprocessname":""}
                url = url[url.find(header)+len(header)+1:]

                ret = url.split("&")
                for i in range(0,len(ret)):
                        if len(ret[i])>0 and ret[i].find('=')!=-1:
                                key,value = ret[i].split("=")
                                if key in data_set :
                                        data_set[key] = value;
                #print "\t".join([data_set["install"],data_set["channel"],data_set["peerid"],data_set["newinstall"],data_set["firstinstallsource"],data_set["firstinstaltime"],data_set["installtime"],data_set["installtype"],data_set["lastuninstalltime"],data_set["firstinstallversion"],data_set["version"],data_set["package_name"],data_set["lastinstallsource"],data_set["fatherprocessname"],fip,ftime])
                print "\t".join([data_set["install"],data_set["peerid"],data_set["installtype"],data_set["newinstall"],data_set["version"],data_set["firstinstallsource"],data_set["lastinstallsource"],data_set["firstinstallversion"],data_set["lastuninstalltime"],data_set["channel"],data_set["firstinstaltime"],data_set["installtime"],data_set["package_name"],data_set["fatherprocessname"],fip,ftime])
        except:
                t,value,traceback = sys.exc_info()
                #print t,value
		#print line
                continue

