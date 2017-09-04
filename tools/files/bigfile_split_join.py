#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun: 大文件分割和合并
    Ref:http://www.cnblogs.com/shenghl/p/3946656.html
    State：未完成
    Date:2017/3/16
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


class CBigF():
    def __init__(self):
        kilobytes = 1024
        megabytes = kilobytes*1000
        self.chunksize = int(200*megabytes)#default chunksize

    # 大文件分割
    def split(self,fromfile,todir):
        print('Splitting',absfrom,'to',absto,'by',chunksize)
        if not os.path.exists(todir):#check whether todir exists or not
            os.mkdir(todir)
        else:
            for fname in os.listdir(todir):
                os.remove(os.path.join(todir,fname))
        partnum = 0
        inputfile = open(fromfile,'rb')#open the fromfile
        while True:
            chunk = inputfile.read(self.chunksize)
            if not chunk:             #check the chunk is empty
                break
            partnum += 1
            filename = os.path.join(todir,('part%04d'%partnum))
            fileobj = open(filename,'wb')#make partfile
            fileobj.write(chunk)         #write data into partfile
            fileobj.close()
        return partnum

    # 小文件合并
    def joinfile(self,fromdir,filename,todir):
        if not os.path.exists(todir):
            os.mkdir(todir)
        if not os.path.exists(fromdir):
            print('Wrong directory')
        outfile = open(os.path.join(todir,filename),'wb')
        files = os.listdir(fromdir) #list all the part files in the directory
        files.sort()                #sort part files to read in order
        for file in files:
            filepath = os.path.join(fromdir,file)
            infile = open(filepath,'rb')
            data = infile.read()
            outfile.write(data)
            infile.close()
        outfile.close()


'''
    测试入口
'''
if __name__=='__main__':
        fromfile  = input('File to be split?')
        todir     = input('Directory to store part files?')
        chunksize = int(input('Chunksize to be split?'))
        absfrom,absto = map(os.path.abspath,[fromfile,todir])
        bf=CBigF()
        try:
            parts = bf.split(fromfile,todir,chunksize)
        except:
            print('Error during split:')
            print(sys.exc_info()[0],sys.exc_info()[1])
        else:
            print('split finished:',parts,'parts are in',absto)