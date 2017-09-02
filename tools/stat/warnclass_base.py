#!/usr/bin/env python27
# -*- coding: utf8 -*-
'''
    功能：监测报警工具基类
    Author:tuling56
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


'''
    监测工具集
'''
class CBaseWarn():
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost",port=3316,user="root", passwd="123")
        self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.cur.execute("use pgv_stat_yingyin")

        # 定义单日跌幅上限和连续跌幅上限
        self.cur_limit=-15
        self.sum_limit=-25

        info='''
            数据库:
                默认数据库是pgv_stat_yingyin,可通过setdb('dbname')设置
            跌幅阈值：
                默认当日跌幅阈值是15%，7日累计跌幅阈值是25%，可通过setlimit(12,30)设置
        '''
        hues.info(info)

    def __del__(self):
        self.cur.close()
        self.conn.close()
        self.fh_summary.close()
        self.fh_detail.close()

    # _报警文件转换成xls
    def _conv2xls(self):
        import xlwt
        workbook=xlwt.Workbook()
        table=workbook.add_sheet('T1')
        self.fh_detail.seek(0)
        contents=self.fh_detail.read().decode('utf8').split('\n')
        for i,v in enumerate(contents):
            lcontent=v.strip().split('\t')
            for j,vv in enumerate(lcontent):
                if isinstance(vv,float):
                    table.write(i,j,vv)
                else:
                    table.write(i,j,vv)
        self.detail_f_xls=re.sub('.txt$',".xls",detail_f)
        workbook.save(self.detail_f_xls)
        hues.success("转化成xls格式成功")

    # _邮件报警
    def _sendemail(self,senddict):
        if os.path.exists(self.summary_f):
            ffsize=os.path.getsize(self.summary_f)
            if ffsize==0:
                print "报警机制开启，但无报警，退出...."
                os.remove(self.summary_f)
                os.remove(self.detail_f)
                sys.exit()
        else:
            print "报警机制开启，但无报警，退出...."

        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sends=senddict.get("sends",[])
        copys=senddict.get("copys",[])

        msg = MIMEMultipart()

        #加邮件头
        msg['to'] = ','.join(sends)
        msg['from'] = 'monitor@cc.sandai.net'
        subject = '%s号%s异常' % (yesterday,self.meaning)
        msg['subject'] = unicode(subject.decode('utf8'))
        if copys:
            msg['Cc'] = ','.join(copys)

        #添加邮件内容
        self.fh_summary.seek(0)
        content=self.fh_summary.read()
        content+="\n详情请查看附件！"
        msg_content = MIMEText(unicode(content.decode('utf-8')), "plain", "utf-8")
        msg.attach(msg_content)

        # 添加附件(解决了中文附件的发送问题)
        self.fh_detail.seek(0)
        att1 = MIMEText(self.fh_detail.read(), 'base64', 'gbk')
        att1["Content-Type"] = 'application/octet-stream'
        fattach=self.detail_f_xls if self.convxls else self.detail_f
        #att1["Content-Disposition"] = "attachment; filename='%s')" %(os.path.basename(fattach)) # 中文附件发送失败
        att1.add_header('Content-Disposition', 'attachment', filename=('gbk','', os.path.basename(fattach).encode('gbk')))
        msg.attach(att1)

        hues.info('[msg to]:',msg['to'])
        hues.info('[attach]:',os.path.basename(fattach))

        #发送邮件
        try:
            server = smtplib.SMTP()
            server.connect('xxxx')
            server.login('xxxx','121212')
            server.sendmail(msg['from'],msg['to'],msg.as_string())
            server.quit()
            hues.success('报警邮件发送成功')
        except Exception, e:
            hues.error('报警邮件发送失败:',str(e))

    # _生成联合sql
    def _gen_join_sql(self,confdict):
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
    def _gen_warn(self,confdict,sql):
        meaning=confdict.get("meaning","")
        itemsdict=confdict.get("itemsdict",{})
        if not meaning or not itemsdict:
            hues.error("配置文件出错")
            return

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

            # 在有报警的情况下才会产生详细的数据表和汇总表
            if iswarn:
                warn_header=u"%s-->%s报警:\t" %(meaning,v)
                warn_sumary=warn_header+' & '.join(warn_sumary)+"\n\n"
                self.fh_summary.write(warn_sumary)
                self.fh_summary.flush()

                self.fh_detail.write(header)
                self.fh_detail.write(warn_detail)
                self.fh_detail.write(warn_sumary)  #在汇总表也详细的加入报警信息
                if not convxls:
                    self.fh_detail.write('-'*50+'\n')
                self.fh_detail.flush()

    def setdb(self, db):
        if 'select' in db or 'delete' in db or 'update' in db or 'drop' in db:
            hues.error(u"所选数据库不能包含mysql关键字")
            return
        self.cur.execute('use %s' % (db))

    def setlimit(self, cur_limit, sum_limit):
        try:
            cur_limit = float(cur_limit.replace('%', ''))
            sum_limit = float(sum_limit.replace('%', ''))
        except Exception, e:
            hues.error(u"阈值设置错误:", str(e))
            return

        self.cur_limit = cur_limit
        self.sum_limit = sum_limit

    ## 报警接口
    def warn(self,confdict,senddict,convxls=False,sendmail=False):
        self.meaning=confdict.get("meaning","")
        self.convxls=convxls
        self.summary_f=u"%s/[异常预警]%s_%s_summary.txt" %(file_path,yesterday,self.meaning)
        self.detail_f=u"%s/[异常预警]%s_%s_detail.txt" %(file_path,yesterday,self.meaning)

        self.fh_summary=open(self.summary_f,'w+')
        self.fh_detail=open(self.detail_f,'w+')

        # 预警产生
        sql=self._gen_join_sql(confdict)
        self._gen_warn(confdict,sql)

        # 预警发送
        if convxls:
            self._conv2xls()
        if sendmail:
            self._sendemail(senddict)


#程序入口
if __name__=="__main__":
    confdict={"meaning":"竞品播放","table":"xmp_jingpin","itemsdict":{'jingpin_pv':"总次数","iqiyi_pv":"爱奇艺",'qq_pv':'腾讯','youku_pv':"优酷"}}
    senddict={"sends":['xxx@xxx.com'],"copys":[]}
    convxls=False
    sendmail=True

    opw=CBaseWarn()
    opw.warn(confdict,senddict,convxls,sendmail)

    '''方式1：直接调用基类的warn方法
    from warnclass_base import CBaseWarn

    mw=CBaseWarn()
    mw.warn('此处按格式写配置即可')

    '''

    '''方法2：继承基类进行扩展
    from warnclass_base import CBaseWarn
    class OnlinePlayWarn(CBaseWarn):
        def online_play_warn(self,confdict....):
            self.warn(....)  # 调用基类的warn方法
    '''


