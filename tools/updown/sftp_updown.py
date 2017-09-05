#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:Python实现sftp的上传和下载文件
    Ref:http://blog.csdn.net/edwzhang/article/details/49502647（改进方向）
    State：完成基于sftp的上传和下载，但还有改进空间
    Date:2017/3/16
    Author:tuling56
'''
import re, os, sys
import hues
import time
import paramiko
import platform

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    SFTP实现文件(夹)的上传和下载
    状态：未完成,中文乱码的问题未解决
'''
class SFTP(object):
    def __init__(self):
        self.sf=paramiko.Transport(sock=('127.0.0.1',122))
        self.sf.connect(username='root',password='123')
        self.sftp=paramiko.SFTPClient.from_transport(self.sf)  #建立一个sftp客户端对象，通过ssh transport操作远程文件


    def __del__(self):
        self.sf.close()
        self.sftp.close()

    # _文件处理工具
    def _getlist(self):
        #ldf=self.sftp.listdir()
        ldi=self.sftp.listdir_iter()
        for file in ldi:
            file_name=file.filename
            isdir=True if file.longname.startswith('d') else False
            file_size=file.st_size
            file_mtime=file.st_mtime
            print "%s-%s-%s-%s" %(file_name,isdir,file_size,time.ctime(file_mtime))

    # sftp文件上传
    def sftp_file_upload(self,local_file,remote_file):
        #Copy a local file (localpath) to the SFTP server as remotepath(要求两端都必须是文件，但可以修改文件名)
        #local_file=r'E:\XMP\Record\Problems\calc_active_newinstall_overlap.sh'
        #remote_file='/tmp/overlap.sh'
        local_file=local_file.decode('gbk').encode('utf-8')
        remote_file=remote_file.decode('gbk').encode('utf-8')
        self.sftp.put(local_file,remote_file)

    # sftp文件下载
    def sftp_file_download(self,local_file,remote_file):
        #Copy a remote file (remotepath) from the SFTP server to the local host(要求两端都必须是文件，但可以修改文件名)
        #local_file=r'D:\\xxx.log'
        #remote_file='/tmp/logrotate.log'
        local_file=local_file.decode('gbk').encode('utf-8')
        remote_file=remote_file.decode('gbk').encode('utf-8')
        self.sftp.get(remote_file,local_file)

    # sftp文件夹下载
    def sftp_dir_download(self,local_dir,remote_dir):
        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)
        self.sftp.chdir(remote_dir)
        RemoteNames = self.sftp.listdir_iter()    # 获取远程文件列表的方法
        for file in RemoteNames:
            filename=file.filename
            fileattr=file.longname
            Local = os.path.join(local_dir, filename)
            if fileattr.startswith('d'):
                self.sftp_dir_download(Local,filename)
            else:
                self.sftp_file_download(Local,filename)
        self.sftp.chdir( ".." )


    # sftp文件夹上传
    def sftp_dir_upload(self,local_dir,remote_dir):
        self.sftp.rmdir(remote_dir)  # 危险！！！！
        if not os.path.isdir(local_dir):
            return False
        LocalNames=os.listdir(local_dir)
        self.sftp.mkdir(remote_dir)
        self.sftp.chdir(remote_dir)
        for local in LocalNames:
            src=os.path.join(local_dir,local)
            if os.path.isdir(src):
                self.sftp_dir_upload(src,local)
            else:
                self.sftp_file_upload(src,local)

        self.sftp.chdir('..')

'''
    SFTP实现文件的上传和下载
    版本：通过ssh执行远程命令获取目录等相关信息
'''
class SFTP_SSHVer(object):
    def __init__(self,host,port,username,passwd):
        # 远程执行
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host,port,username,passwd,timeout=5)

        # 远程传输
        sf = paramiko.Transport((host,port))
        sf.connect(username = username,password = passwd)
        self.sftp = paramiko.SFTPClient.from_transport(sf)
        self.remote_sep="/"
        self.local_sep="\\"

    def __del__(self):
        self.sftp.close()
        self.ssh.close()

    # 平台判定(通过ssh远程执行命令获取，目前还未集成)

    # 平台判定
    def _judge_platform(self):
        systr=platform.system()
        if systr=="Windows":
            print "Windows platform"
        elif systr=="Linux":
            print "Linux platform"
        else:
            print "other platform"

    # 判定远程文件是否是目录
    def _judge_dir(self,dir):
        cmd='if [ -d {dir} ] ;then echo 1;else echo 0; fi'.format(dir=dir)
        #print cmd
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        if len(stderr.read())>0:
            print "%s wrong" %cmd
            return  -1
        res=stdout.read().strip('\n')
        if res=="1":
            return True
        else:
            return False

    # 远程创建目录
    def _remote_mkdir(self,dir):
        cmd='mkdir {dir} && echo 1 ||echo 0'.format(dir=dir)
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        if len(stderr.read())>0:
            print "%s wrong" %cmd
            return  -1
        res=stdout.read().strip('\n')
        if res=="1":
            return True
        else:
            return False

    # 获取远程文件列表(目录为键，名为值)
    def _get_remote_list(self,dir):
        rdf_dict={}
        cmd="cd {dir} && find .  -type f".format(dir=dir)
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        for f in  stdout.readlines():
            f=f.strip("\n").strip('./')
            res=f.split(self.remote_sep)
            if len(res)==1:
                rd='.'
                rf=res[0]
            else:
                rd,rf=res
            rdf_dict.setdefault(rd, []).append(rf)
        return  rdf_dict

    # 接口1: 文件和文件夹上传
    def sftp_upload(self,local,remote):
        try:
            if os.path.isdir(local):                #判断本地参数是目录还是文件
                for root,dirs,files in os.walk(local):
                    for f in files:
                        localf=self.local_sep.join([root,f])
                        remotep=root.replace(local,remote)
                        remotep=remotep.replace(self.local_sep,self.remote_sep)
                        remotef=self.remote_sep.join([remotep,f])
                        if not self._judge_dir(remotep):
                            self._remote_mkdir(remotep)
                        self.sftp.put(localf,remotef)
            else:
                self.sftp.put(local,remote)                #上传文件
        except Exception,e:
            print('upload exception:',str(e))

    # 接口2：文件和文件夹下载
    def sftp_download(self,remote,local):
        try:
            if self._judge_dir(remote):     # 判断远程路径时目录还是文件
                rdf=self._get_remote_list(remote)
                for rd,rf_list in rdf.iteritems():
                    for rf in rf_list:
                        if rd!='.':
                            remotef=self.remote_sep.join([remote,rd,rf])
                            localp=os.path.join(local,rd.replace(self.remote_sep,self.local_sep))
                        else:
                            remotef=self.remote_sep.join([remote,rf])
                            localp=local

                        localf=self.local_sep.join([localp,rf])  # 远程文件存放地址
                        if not os.path.exists(localp):
                            os.makedirs(localp)
                        self.sftp.get(remotef,localf)
            else:
                self.sftp.get(remote,local)
        except Exception,e:
            print('download exception:',str(e))


# 测试入口
if __name__ == "__main__":
    # 基础版
    sftp=SFTP()
    #sftp.getlist()
    #sftp.sftp_file_download('download.log','/tmp/anacron_daily.log')
    #sftp.sftp_file_upload('zhuye.html','/tmp/zhuye.html')

    #sftp.sftp_dir_download('trash','/tmp/subdir')
    sftp.sftp_dir_upload('D:\\Trash\\data xwe','/tmp/trash')

    # SSHVer版本
    #sftp_sshver=SFTP_SSHVer('127.0.0.1',122,'root','123')
    #sftp_tool.sftp_upload("D:\\cygwin64\\home\\yjm\\data\\subdir",'/home/yjm')
    #sftp_sshver.sftp_download('/usr/local/nginx/conf/vhosts','D:\\test')
