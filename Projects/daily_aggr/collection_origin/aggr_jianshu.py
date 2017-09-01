# -*- coding: utf-8 -*-
'''
    Fun:简书收藏和喜欢抓取
    Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
    State：未完成
    Date:2017/4/28
    Author:tuling56
'''
import re,os, sys
import hues
import time
import MySQLdb
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')

import json
import requests
from bs4 import BeautifulSoup


'''
    简书收藏和喜欢抓取
'''
class JianshuAggr():
    def __init__(self):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'labs')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
        self.pattern=re.compile(r'[^\d\s\-【:】]?')  # 替换模式
        self.sess=requests.Session()
        self.cookies_file='jianshu_cookies.ck'
        self.__login()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.sess.close()  #关闭会话

    def _transcode(self, content):
        content = MySQLdb.escape_string(content)
        return content

    # 登录(利用会话来保持cookie)
    def __login(self,post=False):
        if post:
            # 先利用账号和密码进行登录获得cookie
            postdata={"userId":'yueqiulaishu@163.com','passwd':'wba112233'}
            post_url='https://api.weibo.com/oauth2/authorize?client_id=1881139527&redirect_uri=http://www.jianshu.com/users/auth/weibo/callback&response_type=code&state=02d1358fef35ff727e52aa510397aa799a1c05632c2052b6'
            r=self.sess.post(post_url,data=postdata)
            print "服务返回的头部信息:",r.headers
            cookie_dict=requests.utils.dict_from_cookiejar(r.cookies)
            print "服务器返回的cookie:",cookie_dict
            with open(self.cookies_file,'w') as f:
                json.dump(cookie_dict,f,ensure_ascii=False)

        # 将chrome浏览器的cookie为requests库使用
        with open(self.cookies_file,'r') as f:
            try:
                chrome_cookies=json.load(f,encoding='utf-8')#,object_pairs_hook=OrderedDict)
                for ck in chrome_cookies:
                    self.sess.cookies.set(ck['name'],ck['value'])
            except Exception,e:
                hues.error('解析chrome_cookies失败:',str(e))

    # 单条目解析
    def parse_item(self,item):
        source='简书'

        # 解析标题和链接
        try:
            titlehref=item.select('a[class="title"]')[0]
            pageurl=titlehref.attrs.get('href','')
            if pageurl:
                pageurl='https://www.jianshu.com'+pageurl
                m_md5 = hashlib.md5()
                m_md5.update(pageurl)
                pageurlhash = self._transcode(m_md5.hexdigest())
            title=titlehref.string
        except Exception,e:
            print "解析标题和链接失败,",str(e)
            return

        # 解析abstract
        try:
            abstract=item.select('p[class="abstract"]')[0].string.strip().strip('...')
        except Exception,e:
            print "解析abstract失败，",str(e)
            abstract=''

        # 解析publish_time
        try:
            publish_time=item.select('span[class="time"]')[0].attrs.get('data-shared-at','')
            if publish_time:
                publish_time=publish_time[:19].replace('T',' ')
        except Exception,e:
            print "解析publish_time失败:",str(e)
            publish_time=''

        # 解析poster
        try:
            poster=item.select('a[class="wrap-img"] > img')[0]
            poster=poster.attrs.get('src','')
            if poster.startswith('//'):
                poster='http:'+poster
        except Exception,e:
            print "解析poster失败",str(e)
            poster=''

        #　解析read_num和comment_num
        meta=item.select('div[class="meta"] > a')
        read_num=int(meta[0].text.strip('\n').strip())
        comment_num=int(meta[1].text.strip('\n').strip())

         # 入库信息汇总
        hues.info("入库信息============")
        print "title:",title
        print "pageurl:",pageurl
        print "poster:",poster
        print "read_num:",read_num
        print "comment_num:",comment_num
        print "publish_time:",publish_time

        # 数据入库
        try:
            sql="replace into collection_base_info(pageurl,pageurlhash,poster,title,source,abstract,read_num,comment_num,publish_time,insert_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s',%s)"
            paras=(pageurl,pageurlhash,poster,title,source,abstract,read_num,comment_num,publish_time,'now()')
            sql=sql % paras
            hues.log(sql.decode('utf-8').encode('utf-8'))
            m=self.cursor.execute(sql.decode('utf-8').encode('utf-8'))
            print 'replace into collection_base_info:',title,"------>ret = ",m
        except Exception,e:
            hues.warn(str(e))


    # 收藏抓取
    def jianshu_aggr_collect(self):
        # headers可以用也可以不用
        headers={
                    "Referer":"http://www.jianshu.com/bookmarks",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
                }
        collect_url='http://www.jianshu.com/bookmarks'
        res=self.sess.get(collect_url,headers=headers).text
        self.soup=BeautifulSoup(res)
        #print self.soup.prettify().encode('utf8')
        items=self.soup.select('ul[class="note-list"] > li')
        for item in items:
            self.parse_item(item)


    # 喜欢抓取(获取的是html文档)
    def jianshu_aggr_like(self):
        pageno=1
        flag=True
        while flag:
            req_url="http://www.jianshu.com/users/5cb84169d6bb/liked_notes?page=%s" %(pageno)
            hues.info(req_url)
            r=self.sess.get(req_url)
            res_json=r.text
            self.soup=BeautifulSoup(r.text)
            items=self.soup.find_all(id=re.compile('note'))
            if len(items)==0:
                hues.warn("解析结束")
                break
            for item in items:
                self.parse_item(item)
            pageno=pageno+1
            time.sleep(1)


# 测试入口
if __name__ == "__main__":
    jsaggr=JianshuAggr()
    jsaggr.jianshu_aggr_collect()
    jsaggr.jianshu_aggr_like()

