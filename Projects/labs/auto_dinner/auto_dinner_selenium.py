#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:模拟点击进行订餐
	Ref:
	State：
	Date:2017/8/24
	Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

import sqlite3
import json
import urllib2
import cookielib
from selenium import webdriver
from lxml import etree
import time
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup


# 日期参数处理
mdate = date.today().strftime("%Y%m%d")


'''
    模拟点击点餐
'''
class AutoDinnerSelium():
    def __init__(self):
        self.__init_db()
        self.__init_browser()
        self.menus={}

    # 浏览器初始化
    def __init_browser(self,interface=True):
        try:
            profile_dir=r'C:\\Users\\xl\\AppData\\Local\\Google\\Chrome\\User Data'
            chrome_options=webdriver.ChromeOptions()
            if not interface:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_dir))
            self.driver=webdriver.Chrome(chrome_options=chrome_options) # 打开浏览器的时候带cookie
        except Exception,e:
            print "谷歌浏览器初始化失败"
            sys.exit()

    # 数据表初始化
    def __init_db(self):
        self.conn=sqlite3.connect('dinner.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists dinner_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime)')
        self.cursor.execute('create table if not exists history_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime)')
        self.cursor.execute('create table if not exists rank_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime)')

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.driver.quit()
        self.driver.close()

    def __insert_db(self,sql):
        #self.cursor.execute("insert into dinner_info(date,rest,menu,insert_time) values (strftime('%Y%m%d','now'),'美味通','好吃的',datetime())")
        self.cursor.execute(sql)
        self.conn.commit()

    def __save_html(self,fname):
        with open(fname,'w') as f:
            f.write(self.driver.page_source.decode('utf8').encode('utf8'))

    # 订什么餐
    def __dinner(self,menu_name):
        return True

    #　是否订餐成功
    def __check_dinner(self):
        pass

    #　解析菜单
    def parse_menus(self,dinner):
        dinner.click()
        self.__save_html('dinner')

        # 菜单解析
        rests=self.driver.find_elements_by_xpath('//*[@class="rest_wrap"]/section')
        submit=self.driver.find_element_by_xpath('//input[@class="submit_list_btn"]')
        for rest in rests[:-1]:
            dishs=[]
            rest_name=rest.find_element_by_xpath('.//h1[@class="rest_name"]/span')
            rest_name=rest_name.text
            rest_id=rest.get_attribute('id')
            print rest_name,rest_id,"============="
            menus=rest.find_elements_by_xpath('.//a[@class="dish" and @id!=""]')
            for menu in menus:
                menu_name=menu.find_element_by_xpath('./div[@class="dish_name"]/strong').text
                menu_id=menu.get_attribute('id')
                if self.__dinner(menu_name):
                    menu.click()
                    submit.click()
                    if self.__check_dinner():
                        hues.info("订餐成功，定的是什么餐")

                #菜单入库
                print menu_name,menu_id
                dishs.append({"name":menu_name,"id":menu_id})
                sql="replace into menus_info(rest_name,rest_id,dish_name,dish_id,ts) values ('%s','%s','%s','%s',datetime())" %(rest_name,rest_id,menu_name,menu_id)
                self.__insert_db(sql)

            self.menus[rest_name]={"id":rest_id,"dishs":dishs}

        # 菜单保存
        menus=json.dumps(self.menus,encoding="utf8",ensure_ascii=False)
        with open("menus.json",'w') as f:
            f.write(menus)

    # 解析历史
    def parse_history(self,history):
        history.click()
        time.sleep(2)
        flag=True
        isover=False
        while flag or not isover:
            try:
                next_page=self.driver.find_element_by_xpath('//a[@class="turn turn_next"]')
                historys=self.driver.find_elements_by_xpath('//table[@class="history"]/tbody/tr')
                for history in historys[1:]:
                    dinner_num=history.find_element_by_xpath('./td[2]').text
                    dinner_area=history.find_element_by_xpath('./td[3]').text
                    dinner_rest=history.find_element_by_xpath('./td[4]').text
                    dinner_dish=history.find_element_by_xpath('./td[5]').text
                    dinner_time=history.find_element_by_xpath('./td[6]').text
                    print dinner_num,dinner_area,dinner_dish,dinner_time
                    sql="replace into history_info(dinner_num,dinner_area,dinner_rest,dinner_dish,dinner_time,ts) values (%s,'%s','%s','%s','%s',datetime())"
                    paras=(dinner_num,dinner_area,dinner_rest,dinner_dish,dinner_time)
                    sql=sql % paras
                    self.__insert_db(sql)
                flag=False
                if len(historys)<11:
                    isover=True
                else:
                    next_page.click()
                    time.sleep(1)
            except Exception,e:
                hues.warn(str(e))
                history.click()
                time.sleep(1)
                flag=True

    # 解析排行
    def parse_rank(self,ranktag):
        ranktag.click()
        time.sleep(2)
        flag=True
        while flag:
            try:
                ranks=self.driver.find_elements_by_xpath('//section[@class="rank_list"]/ul/li')
                for rank in ranks:
                    rest_name=rank.find_element_by_xpath('.//span[@class="rest_name"]').text
                    dish_name=rank.find_element_by_xpath('.//span[@class="dish_name"]/strong').text
                    dish_taste=rank.find_element_by_xpath('.//span[@class="dish_name"]').text
                    like_num=rank.find_element_by_xpath('.//span[@class="like"]').text.replace(u"喜欢","")
                    rank_num=rank.find_element_by_xpath('.//span[@class="notice"]').get_attribute('id').replace('rank','')
                    print rank_num,rest_name,dish_name,dish_taste
                    sql="replace into rank_info(date,rank,rest_name,dish_name,dish_taste,like_num,ts) values (%s,'%s','%s','%s','%s','%s',datetime())"
                    paras=("strftime('%Y%m%d','now')",rank_num,rest_name,dish_name,dish_taste,like_num)
                    sql=sql % paras
                    self.__insert_db(sql)
                flag=False
            except Exception,e:
                hues.warn(str(e))
                ranktag.click()
                flag=True


    def parse(self):
        self.driver.get('http://dingcan.xunlei.cn/meal/')
        tags=self.driver.find_elements_by_xpath('//nav[@class="nav"]/ul/li')
        for tag in tags:
            print tag.text
            if tag.text==u'餐馆1':
                self.parse_dinner(tag)
            elif tag.text==u'历史':
                self.parse_history(tag)
            elif tag.text==u"排行1":
                self.parse_rank(tag)
            else:
                print "wrong tag"

# 测试入口
if __name__ == "__main__":
    asel=AutoDinnerSelium()
    asel.parse()
