#!/bin/env python
# -*- coding: utf8 -*-

import json
import os,sys

def findpeak(view):
	peakmap = {}
	size = len(view)
	for i in range(1, size - 1):
		if view[i-1] <= view[i] and view[i] >= view[i+1]:
			#print 'findpeak:', i
			#print view[i-1] , view[i], view[i+1]
			peakmap[i+1] = view[i]
			
	return [(k,peakmap[k]) for k in sorted(peakmap.keys())] 
	
if __name__ == '__main__':
	#if len(sys.argv) != 2:
	#	print 'input file!'
	#	exit()
	readfile = 'E:\\Code\\SVN\\trunk\Python\\Projects\\HotView\A48FF45C5BF840DA58690BC6EFE5387DF56EF752.1026430435' #sys.argv[1]
	fname=os.path.split(readfile)[1]
	cid,filesize=fname.split('.')
	print "cid:"+cid+"\nfilesize:"+filesize
	rfb = open(readfile)
	try:
		hot_info = rfb.read( )
	finally:
		rfb.close( )
		
	json_body = json.loads(hot_info)
	view = json_body.get("hot_view")
	#print len(view)
	peakmap = findpeak(view)
	print len(peakmap)
	outstr = ''
	for id, value in peakmap:
		str = '%d\t%d\n' %(id, value)
		outstr = outstr + str
		
	output = '../data/%s.out.txt' %(readfile)
	ofb = open(output, 'w')
	ofb.write(outstr)
	ofb.close( )

	peekmapdict={}
	for i,v in enumerate(peakmap):
		peekmapdict[i]=v
	f=open('peekmap.json','w')
	json.dump(peekmapdict,f)
	f.close()
		
	
	
	

	
