# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：删除表格
'''

import  MySQLdb

#建立连接
conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='hive',db='test') #新建的数据库
if not conn.open:
    print('open %s db fail'%('test_db'))
    exit()
cur=conn.cursor()


'''
  后续处理：删除中间表，关闭连接等
'''
def closePro(conn,cur):
    cur.execute('drop table if exists src_table')
    cur.execute('drop table if exists mid_table1')
    cur.execute('drop table if exists mid_table2')
    cur.execute('drop table if exists xmp_day_play_mid')
    cur.execute('drop table if exists xmp_day_play')
    conn.commit()

    cur.close()
    conn.close()
    print 'relate tables have already been droped!'


if __name__ == "__main__":
    closePro(conn,cur)
