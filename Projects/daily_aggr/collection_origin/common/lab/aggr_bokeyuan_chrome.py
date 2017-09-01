# -*- coding: utf-8 -*-
'''
    Fun:博客园收藏抓取
    Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
    State：
    Date:2017/4/28
    Author:tuling56
'''
import re,os,sys
import hues
import time
import MySQLdb
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

sys.path.append(sys.path[0] + '/../') # 本级目录的上级目录
from chrome_init import ChromeBrowserBase


'''
   博客园收藏抓取
'''
class BokeAggr(ChromeBrowserBase):
    def __init__(self):
        ChromeBrowserBase.__init__(self) # 显示调用父类的初始化方法
        self.init_chrome_browser()      # 调用父类的初始化方法
        #self.init_chrome_cookie('bokeyuan_chrome_cookie.ck')
        #self.driver.get('https://passport.cnblogs.com/user/signin')

    def _transcode(self, content):
        content = MySQLdb.escape_string(content)
        return content

    def process_item(self,item):
        # 初始设置
        type=''
        source='博客园'
        tags=''
        poster=''
        read_num=0
        comment_num=0
        publish_time=''

        # 标题和链接
        try:
            target=item.find_element_by_xpath('.//div[@class="list_block"]/h2/a')
            title=target.text
            pageurl=target.get_attribute("href")
            m_md5 = hashlib.md5()
            m_md5.update(pageurl)
            pageurlhash = self._transcode(m_md5.hexdigest())
        except Exception,e:
            hues.error("解析标题和链接失败:\n"+str(e))
            return

        # 备注
        abstract=''
        try:
            abstract=item.find_element_by_xpath('.//div[@class="link_content"]/div')
            abstract=abstract.text
        except Exception,e:
            hues.warn("无备注:\n"+str(e))

        # types
        tags=''
        try:
            ftags=item.find_elements_by_xpath('.//div[@class="link_memo"]/span[@class="tag"]/a')
            for ftag in ftags:
                tags=tags+"/"+ftag.text
        except Exception,e:
            hues.error("解析类型失败:\n"+str(e))
        tags=tags.strip('/')

        # 入库信息汇总
        hues.info("入库信息============")
        print "title:",title
        print "pageurl:",pageurl
        print "tags:",tags
        print "abstract:",abstract
        print "read_num:",read_num
        print "comment_num:",comment_num

        # 数据入库
        try:
            sql="replace into collection_base_info(pageurl,pageurlhash,title,type,source,abstract,tags,insert_time) values('%s','%s','%s','%s','%s','%s','%s',%s)"
            paras=(pageurl,pageurlhash,title,type,source,abstract,tags,'now()')
            sql=sql % paras
            hues.log(sql.decode('utf-8').encode('utf-8'))
            m=self.cursor.execute(sql.decode('utf-8').encode('utf-8'))
            print 'replace into collection_base_info:',title,"------>ret = ",m
        except Exception,e:
            hues.warn(str(e))

    # 方法１：模拟点击下一页
    def boke_aggr(self):
        self.driver.get('http://wz.cnblogs.com/my/57.html')
        print self.driver.page_source.encode('utf-8')
        next_page=self.driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/a[last()]')
        last=False
        while next_page.text=='Next >' or last:
            cururl=self.driver.current_url
            hues.info("cur crawler:%s" %(cururl))
            items=self.driver.find_elements_by_xpath('//*[@id="wz_list"]/div')
            for item in items:
                self.process_item(item)
            if last:
                break
            next_page.click()
            next_page=self.driver.find_element_by_xpath('//*[@id="main"]/div/div[3]/a[last()]')
            next_url=next_page.get_attribute('href')
            if next_page.text!='Next >':
                last=True

    # 方法2:已实现知道总页数(或通过程序获取)，然后依次遍历
    def boke_aggr_hand(self):
        pass


# 测试入口
if __name__ == "__main__":
    selbrowser=BokeAggr()
    selbrowser.boke_aggr()

