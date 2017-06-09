#!/bin/env python
# -*- coding: utf8 -*-

import sys
import web
import json
from xvr_util import common
import os
from xvr_util import deal_vr_file
from xvr_util import id_map

dest_path='/usr/local/xvr/vod/query/data/'



class Handler:
    def GET(self):
        web.ctx.status = "400"
        print dest_path
        return ""
    
    def POST(self):
        web.ctx.status = "200"
        body_data = web.data()
        if not body_data:
            return self.ret_code(-1,"params error!")
            
        json_body = json.loads(body_data)
        
        vrid         = json_body.get("vrid").encode("utf-8") if json_body.get("vrid") else ""
        type        = json_body.get("type").encode("utf-8") if json_body.get("type") else ""
        operator     = json_body.get("operator").encode("utf-8") if json_body.get("operator") else ""
        file_path    = json_body.get("file_path").encode("utf-8") if json_body.get("file_path") else ""
        file_md5    = json_body.get("file_md5").encode("utf-8") if json_body.get("file_md5") else ""
        
        #subid         = json_body.get("subid").encode("utf-8") if json_body.get("subid") else ""
        subtitle    = json_body.get("subtitle").encode("utf-8") if json_body.get("subtitle") else ""
        forsort        = json_body.get("forsort").encode("utf-8") if json_body.get("forsort") else 0
        source        = json_body.get("source").encode("utf-8") if json_body.get("source") else ""
        filesize    = json_body.get("filesize") if json_body.get("filesize") else 0
        subpay        = json_body.get("subpay").encode("utf-8") if json_body.get("subpay") else ""
        subscore    = json_body.get("subscore").encode("utf-8") if json_body.get("subscore") else ""
        subvotes    = json_body.get("subvotes") if json_body.get("subvotes") else 0
        subvv        = json_body.get("subvv") if json_body.get("subvv") else 0
        subposter    = json_body.get("subposter").encode("utf-8") if json_body.get("subposter") else ""
        refurl        = json_body.get("refurl").encode("utf-8") if json_body.get("refurl") else ""
        playurl        = json_body.get("playurl").encode("utf-8") if json_body.get("playurl") else ""
        level        = json_body.get("level") if json_body.get("level") else 0
        
        specid        = json_body.get("specid") if json_body.get("specid") else 0
        duration    = json_body.get("duration") if json_body.get("duration") else 0
        pixel        = json_body.get("pixel").encode("utf-8") if json_body.get("pixel") else ""
        
        version        = json_body.get("version").encode("utf-8") if json_body.get("version") else ""
        packagename    = json_body.get("packagename").encode("utf-8") if json_body.get("packagename") else ""
        sign        = json_body.get("sign") if json_body.get("sign") else 0
        gearVR        = json_body.get("gearVR") if json_body.get("gearVR") else 0
        online        = json_body.get("online") if json_body.get("online") else 0
        hardware    = json_body.get("hardware") if json_body.get("hardware") else 0
        
        param1        = json_body.get("param1").encode("utf-8") if json_body.get("param1") else ""
        param2        = json_body.get("param2").encode("utf-8") if json_body.get("param2") else ""
        param3        = json_body.get("param3").encode("utf-8") if json_body.get("param3") else ""
        
        status    = 0
        playtype = 1
        
        if vrid == "" or  subtitle == "" or file_path == "" or file_md5 == "" or source == "" or forsort == 0 or type == "" or operator == "":
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
            
        subid = id_map.get_subvrid(vrid, forsort, subtitle, operator)
        print 'subid:',subid
        
        if type == 'video':
            sql = "select count(*) from %s where vrid = '%s'  and forsort = %d and specid =%d " % (tb_subinfo_name,vrid,forsort,specid)
        else:
            sql = "select count(*) from %s where vrid = '%s'  and forsort = %d " % (tb_subinfo_name,vrid,forsort)
        print 'sql:',sql
        ret = common.execute_sql(sql)
        ret = ret[0][0]
        print 'ret:',ret
        if int(ret) > 0:
            return self.ret_code(-1,"record forsort %d exist!" % (forsort))
        
        try:
            dest_file_path = dest_path + os.path.basename(file_path)
            print 'dest_file_path:',dest_file_path
            
            #copy file to local        
            deal_vr_file.rsync_file_tolocal(file_path,dest_file_path)
            
            #check md5            
            if not deal_vr_file.check_file_md5(dest_file_path,file_md5):
                return self.ret_code(-1,"check file md5 failed!")        
            
            #copy file to CDN
            #if map exist
            result, info_map = deal_vr_file.upload_to_cdn(dest_file_path, type)
            if not result:
                return self.ret_code(-1,"copy file to cdn failed!")
            playurl = info_map['playurl']
            filesize = int(info_map['filesize'])
            
        except Exception,e:
            s=sys.exc_info()
            print "error-->%s,line:%s" % (s[1],s[2].tb_lineno)
            return self.ret_code(-1,"unknow error!")
            
        
        if type == 'video':
            tb_subinfo_name = 'xvr_videosub_info'
            diff_fields_name = " ,specid, duration, pixel,"
            diff_fields_value = " ,%d,%d,'%s' , " % (specid, duration, pixel)
        elif type == 'game':
            tb_subinfo_name = 'xvr_gamesub_info'
            diff_fields_name = " ,version,packagename,sign,gearVR, online, hardware,"
            diff_fields_value = " ,'%s','%s',%d,%d,%d,%d , " % (version,packagename,sign,gearVR, online, hardware)
        else:
            tb_subinfo_name = 'xvr_sub_info'
            diff_fields_name = " ,param1, param2, param3,"
            diff_fields_value = " ,'%s','%s','%s' , " % (param1, param2, param3)
                
        try:        
            sql = "insert into " +tb_subinfo_name+"(vrid,subid, subtitle, forsort, source, filesize, subpay, subscore, subvv,subvotes, subposter, refurl, playurl, level,playtype,status "+diff_fields_name+" insert_t) " 
            sql = sql + "values('%s', '%s', '%s', %d, '%s', %d, '%s', '%s', %d, %d, '%s', '%s', '%s', %d, %d, %d "+diff_fields_value+" now()) " 
            sql = sql % (vrid, subid, subtitle, forsort, source, filesize, subpay, subscore, subvv, subvotes, subposter, refurl, playurl, level, playtype, status)
    
            common.execute_sql(sql)        
            
            #change video info 
            if type == 'video':
                sql  = "update " + tb_subinfo_name+" set subscore='%s', subvv=%d, subvotes=%d where subid = '%s'" 
                sql = sql %(subscore, subvv, subvotes, subid)
                common.execute_sql(sql)    
                
            sql  = "select count(distinct(subid)) from %s where vrid = '%s'" % (tb_subinfo_name, vrid) 
            cnt = common.execute_sql(sql)
            cnt = int(cnt[0][0])
            
            sql  = "update xvr_base_info set display= %d where vrid = '%s'" % ( cnt, vrid) 
            common.execute_sql(sql)
            
        except Exception,e:
            s=sys.exc_info()
            print "error-->%s,line:%s" % (s[1],s[2].tb_lineno)
            return self.ret_code(-1,"Add resord failed!")
        
        #add file info to db
        #maintain map base on file
        id_map.add_file_map(info_map['cid'], info_map['filesize'], vrid, subid,operator)
        
        return self.ret_code(1,"")
    
    def ret_code(self, code, msg):
        ret_table = {}
        ret_table["ret"] = code
        ret_table["msg"] = msg
        return json.dumps(ret_table)

