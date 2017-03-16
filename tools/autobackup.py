#!/usr/bin/env python
#-*-coding:utf8-*-

'''
   功能说明:自动备份脚本
'''


import os
import time

source_dir=['/home/yjm/data']
target_dir='/home/yjm/data_backup'

def auto_backup():
    # 如果目标目录不存在，则创建新的目录
    backup_dir=target_dir+'/'+time.strftime("%Y%m%d")
    if os.path.exists(backup_dir):
        print "alwready"
    else:
        os.makedirs(backup_dir)

    backup_file=backup_dir+'/'+time.strftime('%H%M%S')+'.zip'
    zip_command="gzip -qr %s %s" %(backup_file,' '.join(source_dir))  #递归创建压缩包

    if os.system(zip_command)==0:
        print "zip ok!"
    else:
        print "backup fail"


if __name__ == '__main__':
    auto_backup()
