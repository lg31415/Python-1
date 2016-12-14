#!/bin/env python
# -*- coding: utf8 -*-

import sys
#import web
import json
import os
#from xvr_util import common
#from xvr_util import deal_vr_file
#from xvr_util import id_map
#from xvr_util import calc_base_info

dest_path='./data/'

class Handler:
    def GET(self):
        web.ctx.status = "400"
        return ""
    def mgetv(self,vkey):
        web.ctx.status = "200"
        body_data = web.data()
        if not body_data:
            return self.ret_code(-1,"params error!")

        json_body = json.loads(body_data)
        res=json_body.keys(vkey).encode("utf-8") if json_body.get("vrid") else ""
        return res

    
    def POST(self):
        vkeys=map(mgetv,json_body.keys())
        flag=vrid+subtitle+file_path+file_md5+source+forsort+type+operator

        status      = 0
        playtype    = 1
        audit       = 1
        
        if len(flag)==0:
            return self.ret_code(-1,'fields vrid,subtitle,file_path,source, forsort ,type,operator must not empty,please check!')
        
        if not forsort.isdigit() or int(forsort) <= 0:
            return self.ret_code(-1,'forsort must be int and > 0')
            
        #check vrid
        if not vrid[2:].isdigit() or int(vrid[2:]) < 10000000:
            return self.ret_code(-1,"vrid error")
        
        #check base info has vrid or not  
        sql = "select count(*) from xvr_base_info where vrid = '%s'" %(vrid)
        ret = common.execute_sql(sql)
        if int(ret[0][0]) == 0:
            return self.ret_code(-1,"base info table no vrid:%s!" % (vrid))
            
        try:
            download = int(download)
            forsort = int(forsort)
            filesize = int(filesize)
            subvotes = int(subvotes)
            subvv = int(subvv)
            level = int(level)
            specid = int(specid)
            duration = int(duration)
            sign = int(sign)
            gearVR = int(gearVR)
            online = int(online)
            hardware = int(hardware)
        except Exception,e:
            return self.ret_code(-1,"params type error!")
    
        if type == 'video':
            tb_subinfo_name = 'xvr_videosub_info'
        elif type == 'game':
            tb_subinfo_name = 'xvr_gamesub_info'
        else:
            tb_subinfo_name = 'xvr_sub_info'
        
        if type == 'video':
            sql = "select status from %s where vrid = '%s'  and forsort = %d and specid =%d " % (tb_subinfo_name,vrid,forsort,specid)
        else:
            sql = "select status from %s where vrid = '%s'  and forsort = %d " % (tb_subinfo_name,vrid,forsort)
        print 'sql:',sql
        rows = common.execute_sql(sql)
        if rows:
            status = rows[0][0]
            print 'status:',status
            if int(status) >= 0:
                return self.ret_code(-1,"record forsort %d exist!" % (forsort))
            else:
                if type == 'video':
                    sql_del = "delete from %s where vrid = '%s'  and forsort = %d and specid =%d;" % (tb_subinfo_name,vrid,forsort,specid)
                else:
                    sql_del = "delete from %s where vrid = '%s'  and forsort = %d;" % (tb_subinfo_name,vrid,forsort)
                rows = common.execute_sql(sql_del)
            
        
        try:
            dest_file_path = dest_path + os.path.basename(file_path)
            print 'dest_file_path:',dest_file_path
            
            #copy file to local
            if download == 0:
                deal_vr_file.rsync_file_tolocal(file_path, dest_file_path)
            elif download == 1:
                deal_vr_file.download_file(url, dest_file_path)
            
            #check md5
            if not deal_vr_file.check_file_md5(dest_file_path, file_md5):
                return self.ret_code(-1,"check file md5 failed!")        
            
            #copy file to CDN
            result, info_map = deal_vr_file.upload_to_cdn(dest_file_path, type, vrid, forsort, subtitle, operator)
            if not result:
                return self.ret_code(-1,"copy file to cdn failed!")
            playurl = info_map['playurl']
            filesize = int(info_map['filesize'])
            cid = info_map['cid']
            subid = info_map['subid']
            
        except Exception,e:
            s=sys.exc_info()
            print "error-->%s,line:%s" % (s[1],s[2].tb_lineno)
            return self.ret_code(-1,"unknow error!")
            
        
        if type == 'video':
            diff_fields_name = " ,specid, duration, pixel,"
            diff_fields_value = " ,%d,%d,'%s' , " % (specid, duration, pixel)
        elif type == 'game':
            diff_fields_name = " ,version,packagename,picture1,picture2,picture3,picture4,picture5,extra_info,version_log,developer,sign,gearVR,online,hardware,"
            diff_fields_value = " ,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,%d , " % (version,packagename,picture1,picture2,picture3,picture4,picture5,extra_info,version_log,developer,sign,gearVR, online, hardware)
        else:
            diff_fields_name = " ,param1, param2, param3,"
            diff_fields_value = " ,'%s','%s','%s' , " % (param1, param2, param3)
                
        try:        
            sql = "insert into " +tb_subinfo_name+"(vrid, subid, subtitle, forsort, source, filesize, subpay, subscore, subvv, subvotes, subposter, refurl, playurl, level, playtype, status, audit "+diff_fields_name+" insert_t) " 
            sql = sql + "values('%s', '%s', '%s', %d, '%s', %d, '%s', '%s', %d, %d, '%s', '%s', '%s', %d, %d, %d, %d "+diff_fields_value+" now()) " 
            sql = sql % (vrid, subid, subtitle, forsort, source, filesize, subpay, subscore, subvv, subvotes, subposter, refurl, playurl, level, playtype, status, audit)
    
            common.execute_sql(sql)        
            
            #change video info 
            if type == 'video':
                sql  = "update " + tb_subinfo_name+" set subscore='%s', subvv=%d, subvotes=%d where subid = '%s'" 
                sql = sql %(subscore, subvv, subvotes, subid)
                common.execute_sql(sql)    
                
            
        except Exception,e:
            s=sys.exc_info()
            print "error-->%s,line:%s" % (s[1],s[2].tb_lineno)
            return self.ret_code(-1,"Add resord failed!")
        
        #add file info to db
        #maintain map base on file
        id_map.add_file_map(cid, filesize, vrid, subid,operator)
        
        #calc_base_info
        calc_object = calc_base_info.calc_base()
        calc_object.update_base_info('xvr_base_info', vrid, type)
        
        return self.ret_code(1,"")
    
    def ret_code(self, code, msg):
        ret_table = {}
        ret_table["ret"] = code
        ret_table["msg"] = msg
        return json.dumps(ret_table)


if __name__ == '__main__':
    hd=Handler()
    rv=hd.GET()
    print rv
