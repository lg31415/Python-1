#!/usr/bin/env python
# coding: utf-8

import MySQLdb
import time

test_db_host = "127.0.0.1"
test_db_port = 3306
test_db_user = 'root'
test_db_passwd = 'sd-9898w'
test_db_name = 'xvr'
test_db_charset="utf8"


def connect(db_host = test_db_host, db_port = test_db_port, db_user = test_db_user, db_passwd = test_db_passwd, db_name = test_db_name,db_charset=test_db_charset):
    try:    
        conn = MySQLdb.connect(host=db_host, user=db_user, passwd = db_passwd, db = db_name, port=db_port,charset=db_charset)
        return (conn, conn.cursor())
    except:
        return (None, None)

def connect_db(db_host = test_db_host, db_port = test_db_port, db_user = test_db_user, db_passwd = test_db_passwd, db_name = test_db_name,db_charset=test_db_charset):
    conn, cur = connect(db_host, db_port, db_user, db_passwd, db_name,db_charset)
    while conn == None:
        time.sleep(1)
        print "reconnect"
        conn, cur = connect(db_host, db_port, db_user, db_passwd, db_name,db_charset)
    return (conn, cur)    

def close_db_connect(conn_info):
    try:
        conn_info[1].close()
        conn_info[0].close()
    except:
        pass
    
if __name__ == '__main__':
    conn_info = connect_db()
    conn = conn_info[0]
    cur = conn_info[1]
    sql = "select * from xvr_base_info where vrid='vi12345678'"
    print cur.execute(sql)
