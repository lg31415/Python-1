#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append("/usr/local/vod/xvrvideo/pycomm/")
import connect_db
import _mysql_exceptions
from base_conf import xvr_calc_base_conf

class calc_base:
    #private:
    def __init__(self):
        self.__db_info = xvr_calc_base_conf.db_info
        self.__conn_info = self.__get_connect(self.__db_info['host'], self.__db_info['port'], self.__db_info['user'], self.__db_info['passwd'], self.__db_info['name'], self.__db_info['charset'])
        self.__con = self.__conn_info[0]
        self.__cur = self.__conn_info[1]
        self.__audit_denied = xvr_calc_base_conf.audit_denied
        self.__audit_passed = xvr_calc_base_conf.audit_passed
        
    def __del__(self):
        self.__close_connect(self.__conn_info)
    
    def __get_connect(self, host, port, usr, passwd, database, charset):
        conn_info = connect_db.connect_db(host, port, usr, passwd, database, charset)
        
        return conn_info
    
    def __close_connect(self, conn_info):
        connect_db.close_db_connect(conn_info)
        
        return
        
    def __execute_sql(self, sql):
        try:
            self.__cur.execute(sql)
            rows = self.__cur.fetchall()
            self.__con.commit()
        except _mysql_exceptions.OperationalError, e:
            print 'get failed with OperationalError: ' + str(e)
            self.__close_connect(self.__conn_info)
            self.__conn_info = self.__get_connect(self.__db_info['host'], self.__db_info['port'], self.__db_info['user'], self.__db_info['passwd'], self.__db_info['name'], self.__db_info['charset'])
        return rows
    
    def __get_sub_table(self, type):
        if type == 'video':
            return 'xvr_videosub_info'
        elif type == 'game':
            return 'xvr_gamesub_info'
        elif type == 'picture':
            return 'xvr_picturesub_info'
        elif type == 'scene':
            return 'xvr_scenesub_info'
    
        return 'xvr_sub_info'
    
    def __get_max_forsort(self, vrid, sub_table, audit):
        sql_max_forsort = "select max(forsort) from %s where vrid = '%s' and audit = %d and status >= 0;" %(sub_table, vrid, audit)
        rows = self.__execute_sql(sql_max_forsort)
        if not rows or rows[0][0] == None:
            return 0
        max_forsort = rows[0][0]
        
        return max_forsort
    
    def __get_base_pay(self, vrid, sub_table, audit):
        sql_base_pay = "select subpay, subpay_original from %s where vrid = '%s' and audit = %d and status >= 0;" %(sub_table, vrid, audit)
        rows = self.__execute_sql(sql_base_pay)
        pay = 0
        pay_original = 0
        for row in rows:
            subpay, subpay_original = row
            pay += int(subpay)
            pay_original += int(subpay_original)
        
        return pay, pay_original
    
    def __get_base_display(self, vrid, sub_table, audit):
        sql_base_display = "select count(distinct(subid)) from %s where vrid = '%s' and audit = %d and status >= 0;" %(sub_table, vrid, audit)
        rows = self.__execute_sql(sql_base_display)
        if not rows:
            return 0
        display = int(rows[0][0])
        
        return display
        
    def __get_base_filesize_and_source(self, vrid, type, sub_table, max_forsort, audit):
        sql_filesize_source = "select filesize, source from %s where vrid = '%s' and forsort = %d and audit = %d and status >= 0;" %(sub_table, vrid, max_forsort, audit)
        if type == 'video' or type == 'picture':
            sql_filesize_source = "select filesize, source from %s where vrid = '%s' and forsort = %d and audit = %d and status >= 0 order by pixel desc limit 1;" %(sub_table, vrid, max_forsort, audit)
        rows = self.__execute_sql(sql_filesize_source)
        if not rows:
            return 0, ''
        filesize, source = rows[0]
        
        return int(filesize), source
        
    def __get_base_poster_banner_author_uploader(self, base_table, vrid, type, sub_table, max_forsort, audit):
        sql_base = "select poster, banner, author, uploader from %s where vrid = '%s';" %(base_table, vrid)
        rows = self.__execute_sql(sql_base)
        poster, banner, author, uploader = rows[0]
        
        if poster == '':
            sql_sub_poster = "select subposter from %s where vrid = '%s' and forsort = %d and  audit = %d and status >= 0" %(sub_table, vrid, max_forsort, audit)
            if type == 'video' or type == 'picture':
                sql_sub_poster += " order by pixel desc limit 1;"
            rows = self.__execute_sql(sql_sub_poster)
            poster = rows[0][0]
            
        if banner == '':
            sql_sub_poster = "select banner from %s where vrid = '%s' and forsort = %d and  audit = %d and status >= 0" %(sub_table, vrid, max_forsort, audit)
            if type == 'video' or type == 'picture':
                sql_sub_poster += " order by pixel desc limit 1;"
            rows = self.__execute_sql(sql_sub_poster)
            banner = rows[0][0]
            
        if author == '':
            sql_sub_poster = "select author from %s where vrid = '%s' and forsort = %d and  audit = %d and status >= 0" %(sub_table, vrid, max_forsort, audit)
            if type == 'video' or type == 'picture':
                sql_sub_poster += " order by pixel desc limit 1;"
            rows = self.__execute_sql(sql_sub_poster)
            author = rows[0][0]
            
        if uploader == '':
            sql_sub_poster = "select uploader from %s where vrid = '%s' and forsort = %d and  audit = %d and status >= 0" %(sub_table, vrid, max_forsort, audit)
            if type == 'video' or type == 'picture':
                sql_sub_poster += " order by pixel desc limit 1;"
            rows = self.__execute_sql(sql_sub_poster)
            uploader = rows[0][0]
            
        return poster, banner, author, uploader
        
    def __get_base_age_and_publish_t(self, vrid, type, sub_table, max_forsort, audit):
        sql_age_publish_t = "select age, insert_t from %s where vrid = '%s' and forsort = %d and audit = %d and status >= 0" %(sub_table, vrid, max_forsort, audit)
        if type == 'video' or type == 'picture':
            sql_age_publish_t += " order by pixel desc limit 1;"
        rows = self.__execute_sql(sql_age_publish_t)
        age, publish_t = rows[0]
        
        return int(age), publish_t
        
    def __get_base_special(self, vrid, type, sub_table, max_forsort, audit):
        if type == 'video':
            sql_base_special = "select level from %s where vrid = '%s' and forsort = %d and audit = %d and status >= 0 order by pixel desc limit 1;" %(sub_table, vrid, max_forsort, audit)
            rows = self.__execute_sql(sql_base_special)
            if not rows:
                return 0
            level = int(rows[0][0])
            # %d level; %d max_forsort
            special = '%d;%d' %(level, max_forsort)
        elif type == 'game' or type == 'scene':
            sql_base_special = "select packagename, version, hardware from %s where vrid = '%s' and forsort = %d and audit = %d and status >= 0;" %(sub_table, vrid, max_forsort, audit)
            rows = self.__execute_sql(sql_base_special)
            if not rows:
                return ''
            packagename, version, hardware = rows[0]
            # %s packagename; %s version; %d hardware
            special = '%s;%s;%d' %(packagename, version, int(hardware))
        else:
            sql_base_special = "select level from %s where vrid = '%s' and forsort = %d and audit = %d and status >= 0;" %(sub_table, vrid, max_forsort, audit)
            rows = self.__execute_sql(sql_base_special)
            if not rows:
                return 0
            level = int(rows[0][0])
            # %d level
            special = '%d' %(level)
    
        return special
        
    def __clear_base_info(self, base_table, vrid):
        sql_clear_base = "update %s set filesize = 0, update_t = now(), ts = now() where vrid = '%s';" %(base_table, vrid)
        print sql_clear_base
        rows = self.__execute_sql(sql_clear_base)
        
        return rows
    
    #public:
    def update_base_info(self, base_table, vrid, type):
        sub_table = self.__get_sub_table(type)
        max_forsort = self.__get_max_forsort(vrid, sub_table, self.__audit_passed)
        if not max_forsort:
            rows = self.__clear_base_info(base_table, vrid)
            return rows
        
        pay, pay_original = self.__get_base_pay(vrid, sub_table, self.__audit_passed)
        display = self.__get_base_display(vrid, sub_table, self.__audit_passed)  #total episode
        filesize, source = self.__get_base_filesize_and_source(vrid, type, sub_table, max_forsort, self.__audit_passed)
        poster, banner, author, uploader = self.__get_base_poster_banner_author_uploader(base_table, vrid, type, sub_table, max_forsort, self.__audit_passed)
        age, publish_t = self.__get_base_age_and_publish_t(vrid, type, sub_table, max_forsort, self.__audit_passed)
        special = self.__get_base_special(vrid, type, sub_table, max_forsort, self.__audit_passed)
        
        sql_update_base = "update %s set pay = %d, pay_original = %d, display = %d, filesize = %d, age = %d, source = '%s', poster = '%s', banner = '%s', author = '%s', uploader = '%s', publish_t = '%s', special = '%s', update_t = now(), ts = now() where vrid = '%s';" %(base_table, 
        pay, pay_original, display, filesize, age, source, poster, banner, author, uploader, publish_t, special, vrid)
        print sql_update_base
        rows = self.__execute_sql(sql_update_base)
        
        return rows
    
    #private:
    #__db_info
    #__conn_info
    #__con
    #__cur
    #__audit_denied
    #__audit_passed

def run():
    object = calc_base()
    object.update_base_info('xvr_base_info', 'vi10000012', 'video')
    object.update_base_info('xvr_base_info', 'vi10000013', 'picture')
    object.update_base_info('xvr_base_info', 'vi10000014', 'game')

if '__main__' == __name__:
    run()
