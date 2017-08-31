#!/usr/bin/env python27
# -*- coding: utf8 -*-
'''
    功能：在线播放报警
    Author:yuanjunmiao@xunlei.com
    日期：2017年8月30日
'''

import re
import os,sys
import hues
import MySQLdb
from datetime import date, datetime, timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) <= 1:
    yesterday = date.today() - timedelta(days=1)
    yesterday = yesterday.strftime("%Y%m%d")
else:
    yesterday = sys.argv[1]

file_path=os.getcwd()
file_path=file_path.replace("/bin","/data")

# 全局报警文件
fwarn_summary="%s/warn_online_play_sumary_%s.txt" %(file_path,yesterday)
fwarn_detail="%s/warn_online_play_detail_%s.txt" %(file_path,yesterday)


'''
    监测工具集
'''
class CBaseWarn():
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost",port=3316,user="root", passwd="123")
        self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.cur.execute("use pgv_stat_yingyin")

        # 数据生成
        self.fsummary=open(fwarn_summary,'w+')
        self.fdetail=open(fwarn_detail,'w+')

        # 定义单日跌幅上限和连续跌幅上限
        self.cur_limit=-15
        self.sum_limit=-25

    def __del__(self):
        self.cur.close()
        self.conn.close()
        self.fsummary.close()
        self.fdetail.close()

    # _报警文件转换成xls
    def _conv2xls(self):
        import xlwt
        data=xlwt.Workbook()
        table=data.add_sheet('T1')
        self.fdetail.seek(0)
        contents=self.fdetail.read().decode('utf8').split('\n')
        for i,v in enumerate(contents):
            lcontent=v.strip().split('\t')
            for j,vv in enumerate(lcontent):
                if isinstance(vv,float):
                    table.write(i,j,vv)
                else:
                    table.write(i,j,vv)
        self.fwarn_detail_xls=re.sub('.txt$',".xls",fwarn_detail)
        data.save(self.fwarn_detail_xls)

    # _邮件报警
    def _sendemail(self,tabledict,senddict,xls=False):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        meaning=tabledict.get("meaning","")
        sends=senddict.get("sends",[])
        copys=senddict.get("copys",[])

        msg = MIMEMultipart()

        #加邮件头
        msg['to'] = ','.join(sends)
        msg['from'] = 'monitor@cc.sandai.net'
        subject = '%s号%s异常' % (yesterday,meaning)
        msg['subject'] = unicode(subject.decode('utf8'))
        if copys:
            msg['Cc'] = ','.join(copys)

        #添加邮件内容
        self.fsummary.seek(0)
        content=self.fsummary.read()
        content+="\n详情请查看附件！"
        msg_content = MIMEText(unicode(content.decode('utf-8')), "plain", "utf-8")
        msg.attach(msg_content)

        # 添加附件
        self.fdetail.seek(0)
        att1 = MIMEText(self.fdetail.read(), 'base64', 'gb2312')
        att1["Content-Type"] = 'application/octet-stream'
        fattach=self.fwarn_detail_xls if xls else fwarn_detail
        att1["Content-Disposition"] = 'attachment; filename="%s"' % (os.path.basename(fattach))
        msg.attach(att1)

        hues.info('[msg to]:',msg['to'])
        #发送邮件
        try:
            server = smtplib.SMTP()
            server.connect('xxxx')
            server.login('xxxxx','121212')
            server.sendmail(msg['from'],msg['to'],msg.as_string())
            server.quit()
            hues.success('邮件发送成功')
        except Exception, e:
            hues.error('邮件发送失败',str(e))


    # _生成联合sql
    def _magicconv(self,confdict):
        table=confdict["table"]
        selects=confdict["itemsdict"].keys()
        single_select_options="date,"+','.join(selects)

        join_select_options=['a.date','b.date']
        for item in selects:
            #statitem="a.%s,b.%s,concat(round((a.%s-b.%s)*100/b.%s,2),'%%')" %(item,item,item,item,item)  # 百分表示方法
            statitem="a.%s,b.%s,round((a.%s-b.%s)*100/b.%s,2) as %s_wr" %(item,item,item,item,item,item)
            join_select_options.append(statitem)
        join_select_options=','.join(join_select_options)

        tbla="select %s from %s where date>=date_sub(curdate(),interval 7 day)" %(single_select_options,table)
        tblb="select %s from %s where date>=date_sub(curdate(),interval 14 day)" %(single_select_options,table)
        cond=" b.date=date_format(date_sub(a.date,interval 7 day),'%Y%m%d') order by a.date desc"
        sql = "select {join_select_options} from ({tbla}) a inner join ({tblb}) b on {cond}".format(join_select_options=join_select_options,tbla=tbla,tblb=tblb,cond=cond)

        return sql

    # _查询和报警处理
    def _magicwarn(self,confdict,sql):
        meaning=confdict.get("meaning","")
        itemsdict=confdict.get("itemsdict",{})
        self.cur.execute(sql)
        results = self.cur.fetchall()
        for k,v in itemsdict.iteritems():
            # 要为每个统计项添加header头
            header=["日期(上周同期)",v+"\t上周同期"+v,v+"周同比（%）"]
            header='\t'.join(header)+'\n'
            iscur,downnum,maxdown,sumdown=0,0,0,0
            warn_detail=''
            warn_sumary=[]
            for itemres in results:
                warn_detail+=itemres['date']+'('+itemres['b.date']+')\t'+'\t'.join(map(lambda s:str(s),[itemres[k],itemres["b."+k],itemres[k+"_wr"]]))+'\n'
                weekratio=float(itemres[k+"_wr"])
                if iscur==0:
                    cur_weekratio=weekratio
                    iscur=1
                sumdown+=weekratio
                if weekratio<0:
                    downnum+=1
                maxdown=weekratio if maxdown>weekratio else maxdown

            # 汇总数据
            #hues.info("[downnum]:",downnum,"[maxdown]:",maxdown,"[sumdown]:",sumdown)
            warn_detail+="\t".join(["[downnum]:"+str(downnum),"[maxdown]:"+str(maxdown)+"%","[sumdown]:"+str(sumdown)+"%"])+"\n"

            iswarn=False
            if downnum==7:
                warn=u"连续七日周同比下跌"
                warn_sumary.append(warn)
                iswarn=True

            if cur_weekratio<self.cur_limit:
                warn=u"昨日跌幅超过"+str(abs(self.cur_limit))+'%'
                warn_sumary.append(warn)
                iswarn=True

            if sumdown<self.sum_limit:
                warn=u"近七日跌幅和超过"+str(abs(self.sum_limit))+'%'
                warn_sumary.append(warn)
                iswarn=True

            # 在有报警的情况下才会产生详细的数据表
            if iswarn:
                warn_header=u"%s-->%s报警:\t" %(meaning,v)
                warn_sumary=warn_header+' & '.join(warn_sumary)+"\n\n"
                self.fsummary.write(warn_sumary)
                self.fsummary.flush()

                self.fdetail.write(header)
                self.fdetail.write(warn_detail)
                self.fdetail.write(warn_sumary)  #在汇总表也详细的加入报警信息
                self.fdetail.write('-'*50)
                self.fdetail.flush()

    ## 报警接口
    def api_warn(self,confdict):
        sql=self._magicconv(confdict)
        self._magicwarn(confdict,sql)


    # 播放统计报警按站点
    def online_play_warning(self,xls=False,sendmail=True):
        confdict={"meaning":"竞品播放","table":"xmp_jingpin","itemsdict":{'jingpin_pv':"总次数","iqiyi_pv":"爱奇艺",'qq_pv':'腾讯','youku_pv':"优酷"}}
        senddict={"sends":['xxxx@xxx.com'],"copys":[]}
        self.api_warn(confdict)
        if xls:
            self._conv2xls()
        if sendmail:
            self._sendemail(confdict,senddict,xls=False)



#程序入口
if __name__=="__main__":
    opw=CBaseWarn()
    opw.online_play_warning()


