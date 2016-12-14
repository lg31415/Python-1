#!/usr/bin/env python
#-*-coding:utf8-*-

'''
   功能说明:自动备份脚本,可以作为SVN的辅助手段
'''


import os
import time

source_dir=['C:\\Users\\yjm\\Downloads\\Documents\\testdir']
target_dir='C:\\Users\\yjm\\Downloads\\Documents\\backup'

def backfile():
    # 如果目标目录不存在，则创建新的目录
    backup_dir=target_dir+'\\'+time.strftime("%Y%m%d")
    if os.path.exists(backup_dir):
        print "target dir alwready"
    else:
        os.makedirs(backup_dir)

    backup_file=backup_dir+'\\'+time.strftime('%H%M%S')+'.zip'
    print(''.join(source_dir),backup_file)
    zip_command="zip -r %s %s" %(backup_file,' '.join(source_dir))  #递归创建压缩包

    if os.system(zip_command)==0:
        print "zip ok!"
    else:
        print "backup fail"


if __name__ == '__main__':
    backfile()
