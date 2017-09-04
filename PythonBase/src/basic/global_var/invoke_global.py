#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Date:
    Author:tuling56
'''
import os
import sys
import copy
#print sys.getdefaultencoding()

reload(sys)
sys.setdefaultencoding('utf-8')

os.environ['KK_WORKSPACE']="/usr/local/sandai/server"
ENV_KK_WORKSPACE=os.environ['KK_WORKSPACE']
common_dir=ENV_KK_WORKSPACE+"/bin/common"
sys.path.append(common_dir)

import global_var as G_VAR
sys.exit(0)

import global_env as G_ENV

# 调用和修改全局变量
def invoke_global_var():
    G_ENV.g_maillist.append('this is append')
    print G_ENV.g_maillist

# 调用全局函数
def invoke_gloabl_fun():
    G_ENV.load_config()
    twin0551_conn,twin0551_cursor = G_ENV.open('twin0551')

    date,hour="20161001","23"
    sql="select * from kk_stat_dim.tbls_conf"
    cursor = None
    n = twin0551_cursor.execute(sql)
    for row in twin0551_cursor.fetchall():
        (fmachine,fdb,ftbl,fsplit,fcolumns,fjdbcurl,fuser,fpsd,fid,frsync_machine,fdest_path,frsync_prex) = row            
        table = "%s_%s%s%s" % (ftbl,date,fsplit,hour)
        for db in fdb.split(','):
            try:
                sql = "insert into kk_stat_dim.rsync_put_context(Fid,Fdb,Fdate,Fhour,Frsync_status) values(%s,%s,%s,%s,-1)"
                param = (fid,db,date,hour)
                n = twin0551_cursor.execute(sql,param)   
            except Exception,e:
                (type, value, traceback) =  sys.exc_info()
                print type,value,traceback,e
                continue
    G_ENV.close(twin0551_conn,twin0551_cursor)
    


if __name__ == "__main__":
    pass


