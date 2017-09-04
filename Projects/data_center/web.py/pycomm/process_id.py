#!/usr/bin/env python
# coding: utf-8

import connect_db 

def reset_id(db_info, table, begin_id):
    sql_drop = 'drop table if exists %s'%(table)
    sql_create_table = 'create table if not exists %s (id bigint auto_increment primary key, operator varchar(20) default "") auto_increment=%d;'%(table, begin_id)
    conn_info = connect_db.connect_db(db_info['host'], db_info['port'], db_info['user'], db_info['passwd'], db_info['name'])
    conn = conn_info[0]
    cur = conn_info[1]
    cur.execute(sql_drop)
    cur.execute(sql_create_table)
    conn.commit()
    connect_db.close_db_connect(conn_info)    
    
def new_id(db_info, table, operator = ''):
    sql_lock_table = 'lock table %s WRITE;'%(table)
    sql_insert_id = 'insert into %s(operator) values("%s");'%(table, operator)
    sql_get_id = 'select max(id) from %s;'%(table)
    sql_unlock_table = 'unlock tables;'

    conn_info = connect_db.connect_db(db_info['host'], db_info['port'], db_info['user'], db_info['passwd'], db_info['name'])
    conn = conn_info[0]
    cur = conn_info[1]
    
    cur.execute(sql_lock_table)
    cur.execute(sql_insert_id)
    cur.execute(sql_get_id)
    conn.commit()
    rows = cur.fetchall()
    if len(rows) == 0:
        assert(0)
    ret_id =  rows[0][0]
    
    cur.execute(sql_unlock_table)

    connect_db.close_db_connect(conn_info)
    return ret_id
    
    
if __name__ == '__main__':
    print "Carefully"
    #reset_id('vrid_list', 10000001)
    
