## 文件操作工具

[TOC]

### 同步

#### autorsync

基于paramiko和watchdog的文件（夹）自动同步工具，在win<-->linux平台上自动同步，其中watchdog用以监测文件的变化，如修改，删除，添加等操作



### 上传和下载

#### sftp_updown.py

基于sftp的文件和文件夹上传和下载，还需要对路径进行完善，能否直接下载整个目录

例子

```
比如下载远程文件夹：/usr/local/downdir 到本地的/home/yjm/todir
python sftp_updown.py /usr/local/downdir /home/yjm/todir
只会将远程的downdir目录下的所有内容（不包含downdir本身），下载到在本地的todir目录下，不会在todir目录下创建downdir目录
```



## 参考

