#!/bin/env python
#coding:utf-8
import sys
sys.path.append("/usr/local/res_processor/third_party")
import get_increase_data
import common
import break_relation
import id_mapping
import MySQLdb
import dump
from synchronization_kankan import Synchronous_kankan


def force_douban_match(movieid, douban_id, auditor):
    sql = "select pageurlhash from douban_base_info where  pageurl like '%%/subject/%s%%';"%(douban_id)
    exists_list = common.execute_sql(sql, db_name = "gspider_4503")
    if len(exists_list) != 1:
        exists_list = common.execute_sql(sql, db_name = "crawler")
    if len(exists_list) != 1:
        content = "new douban_id not in db"
        print content
        return False, content

    break_relation.break_douban_relation(movieid)
    id_mapping.map_id(movieid, douban_id, "subject", "douban")
    sql = "update media_base_info set douban_id='%s' where movieid='%s';"%(douban_id, movieid)
    common.execute_sql(sql)

    sql = "update media_info_search set douban_id='%s' where movieid='%s';"%(douban_id, movieid)
    common.execute_sql(sql)

    sql = sql.replace("media_info_search", "media_info_search_pc")
    common.execute_sql(sql)

    auditor = MySQLdb.escape_string(auditor)
    sql = "update media_audit set audit_status=%d, auditor='%s', audit_time=NOW() where old_media_id='%s' and source='douban';"%(common.AUDIT_OK, auditor, douban_id)
    common.execute_sql(sql, db_name = "media_audit")

    return True, ""

def force_third_party_match(movieid, pageurlhash, auditor):
    sql = "select source from third_party_base_info where pageurlhash='%s';"%(pageurlhash)
    ret_list = common.execute_sql(sql, db_name = "lichao")
    if len(ret_list) != 1:
        content = "not have this key: %s in third_party_base_info"%(pageurlhash)
        print content
        return False, content

    site = ret_list[0][0]
    #break_relation.break_third_party_relation(movieid, site)
    sql = 'select * from id_mapping where media_id = "%s" and  old_id="%s" and old_source = "%s" and type = "info"'%(movieid, pageurlhash, site)
    existlist = common.execute_sql(sql, db_name = "lichao")
    if len(existlist) ==0  :
        sql = "insert into id_mapping values('%s', '%s', 'info', '%s');"%(movieid, pageurlhash, site)
        common.execute_sql(sql, db_name = "lichao")
    else:
        print 'id_mapping 关联已经存在 movieid : %s , pageurlhash : %s , site : %s'%(movieid, pageurlhash, site)

    rd = get_increase_data.ResourceData()
    ok ,err =  rd.load_resource_data(movieid, pageurlhash)
    if ok:
        auditor = MySQLdb.escape_string(auditor)
        sql = "update media_audit set audit_status=%d, auditor='%s', audit_time=NOW() where old_media_id='%s' and source='%s';"%(common.AUDIT_OK, auditor, pageurlhash, site)
        common.execute_sql(sql, db_name = "media_audit")

    return ok, err
