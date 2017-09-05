## 文件操作工具

[TOC]

### 同步

分为自动同步和定时同步

#### auto_rsync

基于paramiko和watchdog的文件（夹）自动同步工具，在win<-->linux平台上自动同步，其中watchdog用以监测文件的变化，如修改，删除，添加等操作

#### fabric_rsync

基于轻量级监控库fabric的文件和文件夹同步工具，但不能自动监测，需要定时启动

### 上传和下载

#### web_download.py

网络文件下载，基于urllib2实现，还有其它很多的库可选，目前暂时只实现了urllib2

#### sftp_updown.py

基于sftp的文件和文件夹上传和下载，还需要对路径进行完善，能否直接下载整个目录

例子:

```shell
#比如下载远程文件夹：/usr/local/downdir 到本地的/home/yjm/todir
python sftp_updown.py /usr/local/downdir /home/yjm/todir
#注意：只会将远程的downdir目录下的所有内容（不包含downdir本身），
#	  下载到在本地的todir目录下，不会在todir目录下创建downdir目录
```

> 目前使用的远程执行bash命令的方式，需要改装成自带库函数实现

#### ftp_updown.py

基于ftplib的文件上传和下载，支不支持文件夹的上传和下载？

```python
# ftp相关操作命令
ftp.cwd(pathname) #设置FTP当前操作的路径
ftp.dir() #显示目录下文件信息
ftp.nlst() #获取目录下的文件
ftp.mkd(pathname) #新建远程目录
ftp.pwd() #返回当前所在位置
ftp.rmd(dirname) #删除远程目录
ftp.delete(filename) #删除远程文件
ftp.rename(fromname, toname)#将fromname修改名称为toname。
ftp.storbinaly("STOR filename.txt",file_handel,bufsize) # 上传目标文件
ftp.retrbinary("RETR filename.txt",file_handel,bufsize) # 下载FTP文件
```

> 还存在一些问题

#### scp_updown.py

基于scp的文件上传和下载，支不支持文件夹的上传和下载？

> 集成实现在sftp中，没有单独的模块



## 参考

[ftp文件上传和下载](http://blog.csdn.net/linda1000/article/details/8255771)

[基于ssh的sftp文件上传和下载](http://blog.csdn.net/edwzhang/article/details/49502647)

[sftp命令官方参考](https://paramiko-docs.readthedocs.io/en/1.15/api/sftp.html)