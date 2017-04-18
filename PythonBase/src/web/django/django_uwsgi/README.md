# 该目录是django项目目录,项目名:django_nginx
.
├── app_content		# django项目的一个app
├── app_welcome  	# django项目的一个app
├── django_project	# django项目的配置文件
├── db.sqlite3		# django项目的数据库文件
├── django_wsgi.py	# 用uWSGI代替django默认的web服务器(有问题，暂时未使用)
├── log				# uwsgi指定的日志目录
├── manage.py		# django项目的项目管理文件
├── README.md        			
├── django_uwsgi.sh	# uwsgi启动程序

uwsgi+django+nginx 之间的关系是怎样的？

#解决过程：
#1.uwsgi+nginx
#   uwsgi启动服务，配置nginx，将指定端口的内容发给uwsgi进行处理，(其实后台是python程序进行处理)
