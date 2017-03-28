#!/usr/bin/env python
# coding: utf-8

class short_video_conf:
	db_info = {
		'host':'127.0.0.1',
		'port':3306,
		'user':'root',
		'passwd':'sd-9898w',
		'name':'svideo',
		'charset':'utf8'
	}
	
	rsync = '/usr/bin/rsync'
	rsync_usr = 'svideo'
	edit_rsync_ip = '10.10.200.192:8873'    #编辑后台机器
	edit_rsync_module = 'svideo'                            #编辑后台rsync模块
	rsync_psdfile = '/etc/rsync.pass.192'

	file_root_path = '/usr/local/vod/svideo/videoata'
	audit = {
		"poster_local_url_prefix":'http://10.10.160.11:8089',
		"video_local_url_prefix":'http://10.10.160.11/player.swf?type=http&file='
	}
	ffmpeg_tool = '/usr/local/bin/ffmpeg'

class xvr_media_conf:
        db_info = {
                'host':'127.0.0.1',
                'port':3306,
                'user':'root',
                'passwd':'sd-9898w',
                'name':'xvr',
                'charset':'utf8'
        }
