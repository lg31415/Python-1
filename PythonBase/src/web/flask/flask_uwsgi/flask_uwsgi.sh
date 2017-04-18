#!/bin/bash
cd `dirname $0`

#set -x
set -e

echo -e "\e[1;31mkill uwsgi runing...\e[0m"
pid=$(ps -ef| grep "uwsgi" |awk '/threads/{print $2}')
for i in $pid;do
	echo "kill uwsgi,pid:$i" 
	kill -9 "$i"
done

echo -e "\e[1;31mstart uwsgi.....\e[0m."
/usr/sbin/uwsgi --enable-threads --ini ./flask_uwsgi.ini  --buffer-size=32768 --post-buffering=4096 

exit 0
