#!/usr/bin/env python
# coding: utf-8

from __future__ import division
import os
import sys
sys.path.append("/usr/local/vod/pycomm/")
from base_conf import short_video_conf
import file_info

def screenshot(media_path, interval = 10):
    tool = short_video_conf.ffmpeg_tool
    dest_dir = file_info.get_basename(media_path)
    if not file_info.exists_path(dest_dir):
        cmd = 'mkdir -p %s' %(dest_dir)
        print cmd
        if os.system(cmd) != 0:
            print "failed to run cmd=%s" %cmd
            return False
            
    os.system('rm -rf %s/*.jpg' % (dest_dir,)) 
    
    cmd = '%s -ss 00:00:00 -i %s -y -f image2 -vf fps=fps=1/%d  %s/%%3d.jpg' %(tool, media_path, interval, dest_dir)
    print cmd
    if os.system(cmd) != 0:
        print "failed to run cmd=%s" %cmd
        return False
        
    return True

if __name__ == '__main__':
    screenshot('/home/luochuan/test/ffmpeg/a1aeaad6a0bf7480e1dbd916bb6825d1dcd08647_16473472.flv', 5)
    print "Carefully"
    #screenshot('')
