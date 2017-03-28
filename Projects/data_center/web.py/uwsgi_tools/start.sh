#!/bin/bash
#/usr/local/python27/bin/uwsgi --enable-threads  --ini conf/vod.conf --buffer-size=32768 --post-buffering=4096
killall -9 uwsgi
sleep 1
/usr/bin/uwsgi --enable-threads  --ini uwsgi_webpy.conf --buffer-size=32768 --post-buffering=4096
sleep 2

ps -ax | grep vod
