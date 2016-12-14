#!/bin/env/pyhton
#-*-coding:utf8-*-
'''
   功能说明：将txt文件转存成excel
'''
import xlwt
import sys

def txt2xls(inputfile,outputexcel):
    #Excel
    data=xlwt.Workbook()         
    table=data.add_sheet('T1')   

    f=open(inputfile,'r')
    contents=f.read().decode('utf8').split('\n')
    #contents=f.readlines()
    for i,v in enumerate(contents):
        lcontent=v.strip().split()
        for j,vv in enumerate(lcontent):
            if isinstance(vv,float):
                table.write(i,j,vv)
            else:
                table.write(i,j,vv)
    data.save(outputexcel)

if __name__ == '__main__':
    if(len(sys.argv)==1):
        print 'please input file:'
        sys.exit(-1)
    inputfile=sys.argv[1]
    outputexcel=inputfile.split('.')[0]+'.xls'
    txt2xls(inputfile,outputexcel)
    