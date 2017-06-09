#!/bin/bash
cd `dirname $0`

pid=$(ps -ef| grep uwsgi | awk '/threads/{print $2}')
for i in $pid;do
	echo "kill uwsgi,pid:"$i
	kill -9 $i
done

echo "start uwsgi......"
/usr/bin/uwsgi --enable-threads --ini datacenter_uwsgi.ini --buffer-size=32768 --post-buffering=4096
#/usr/bin/uwsgi --loop gevent --ini datacenter_uwsgi.ini --buffer-size=32768 --post-buffering=4096


exit 0
