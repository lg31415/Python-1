# -*- coding: utf-8 -*-
'''
    Fun:今日头条收藏抓取
    Ref:http://blog.csdn.net/qq_30242609/article/details/70859891
    State：
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

from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.common.keys import Keys


'''
   今日头条收藏抓取
'''
class ToutiaoAggr():
    def __init__(self,interface=False,browser='Chrome'):
        self.conn=MySQLdb.connect(host = 'localhost', port = 3316, user = 'root', passwd = '123', db = 'labs')
        self.cursor = self.conn.cursor()
        self.cursor.execute('set names utf8')
        self.pattern=re.compile(r'[^\d\s\-:]?')  # 替换模式
        self._init_browser(interface,browser)

    # 浏览器初始化
    def _init_browser(self,interface,browser):
        if browser=='Chrome':
            profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Google\\Chrome\\User Data'
            chrome_options=webdriver.ChromeOptions()
            if not interface:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
            self.driver=webdriver.Chrome(chrome_options=chrome_options) # 打开浏览器的时候带cookie
        elif browser=='Firefox':
            profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Mozilla\\Firefox\\Profiles\rh7qc3tr.default'
            profile_option=webdriver.FirefoxProfile(profile_dir)
            self.driver=webdriver.Firefox(profile_option)
        else:
            print "wrong browser parammeters"
            sys.exit()
        #self.driver.maximize_window()
        hues.info("浏览器初始化完毕")

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.driver.quit()
        self.driver.close()

    def _transcode(self, content):
        content = MySQLdb.escape_string(content)
        return content

    def _scroll(self,scroll_num):
        hues.info("滚动下滑，继续抓取......")
        scroll_dis=10000*scroll_num
        js="var q=document.body.scrollTop=%s" %(scroll_dis)        # chrome浏览器
        self.driver.execute_script(js)
        time.sleep(4)

    def process_item(self,item):
        # 初始设置
        type=''
        source='今日头条'
        tags=''
        abstract=''
        poster=''
        read_num=0
        comment_num=0
        publish_time=''

        # 标题和链接
        try:
            target=item.find_element_by_xpath('div/div[1]/div/div[1]/a')
            title=target.text
            pageurl=target.get_attribute("href")
            m_md5 = hashlib.md5()
            m_md5.update(pageurl)
            pageurlhash = self._transcode(m_md5.hexdigest())
        except Exception,e:
            hues.error("解析标题和链接失败:\n"+str(e))
            return

        # 海报
        try:
            poster=item.find_element_by_xpath('div/div[2]/a/img')
            if poster:
                poster=poster.get_attribute("src")
            else:
                poster=''
        except Exception,e:
            hues.error("解析海报失败:\n"+str(e))


        # 阅读量、评论量、发表日期
        try:
            attach_info=item.find_element_by_xpath('div/div[1]/div/div[2]')
            read_num=attach_info.find_element_by_xpath('div[1]/a[1]')
            if read_num:
                read_num=read_num.text
                m=re.search('\d+',read_num)
                if m:
                    read_num=m.group(0)
                else:
                    read_num=0
            else:
                read_num=0

            comment=attach_info.find_element_by_xpath('div[1]/a[2]')
            if comment:
                comment=comment.text
                comment_num=re.sub(self.pattern,'',comment).strip()
            else:
                comment_num=0

            publish_time=attach_info.find_element_by_xpath('div[1]/span')
            if publish_time:
                publish_time=publish_time.text
                publish_time=re.sub(self.pattern,'',publish_time).strip()
            else:
                publish_time=''
        except Exception,e:
            hues.error("解析阅读量、评论量、发布日期失败:\n"+str(e))


        # 入库信息汇总
        print "title:",title
        print "pageurl:",pageurl
        print "read_num:",read_num
        print "comment_num:",comment_num
        print 'publish_time:',publish_time

        # 数据入库
        sql="replace into collection_base_info(pageurl,pageurlhash,poster,title,type,source,abstract,tags,read_num,comment_num,publish_time,insert_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s)"
        paras=(pageurl,pageurlhash,poster,title,type,source,abstract,tags,str(read_num),str(comment_num),publish_time,'now()')
        sql=sql % paras
        hues.info(sql.encode('utf-8'))
        m=self.cursor.execute(sql.encode('utf-8'))
        print 'replace into collection_base_info:',title,"------>ret = ",m


    # 方法１：模拟滚动
    def scroll_aggr(self):
        self.driver.get('http://www.toutiao.com/c/user/3163731884/?tab=favourite')

        #　切换到收藏页
        collecton_tab=self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[1]/ul/li[2]')
        collecton_tab.click()
        self.driver.implicitly_wait(3)

        start,scroll_num=0,1
        now_total_num,pre_total_num=0,0
        while True:
            if scroll_num!=1:
                self._scroll(scroll_num)
            items=self.driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div/ul/li')
            now_total_num=len(items)
            start_pos=start
            hues.info("now_total_num:"+str(now_total_num))
            hues.info("start_pos:"+str(start_pos))
            if now_total_num==pre_total_num:
                hues.warn("没有更新内容,尝试再次刷新.....")
                self._scroll(scroll_num)
                items=self.driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div[2]/div/div[3]/div/ul/li')
                now_total_num=len(items)
                if now_total_num==pre_total_num:
                    hues.error("再次刷新后依然没有抓取到新内容，退出")
                    break
            for item in items[start_pos:]:
                self.process_item(item)
                start=start+1
            pre_total_num=now_total_num
            scroll_num=scroll_num+1

        # 模拟请求
        def moni_aggr(self):
            pass
            '''
                url='http://www.toutiao.com/c/user/favourite/?page_type=2&user_id=3163731884&max_behot_time=0&count=20&max_repin_time=1501561747'
                self.driver.get()
            '''

# 测试入口
if __name__ == "__main__":
    selbrowser=ToutiaoAggr(interface=True,browser='Chrome')
    selbrowser.scroll_aggr()

