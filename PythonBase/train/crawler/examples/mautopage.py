#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun: 翻页加载的实现
	Ref: http://www.tuicool.com/articles/22eY7vQ
	Author:tuling56
	Date:
'''
import os,sys
import time
from datetime import date, datetime, timedelta
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

# 日期参数处理
if len(sys.argv) <= 1:
	yesterday = date.today() - timedelta(days=1)
	yesterday = yesterday.strftime("%Y%m%d")
else:
	yesterday = sys.argv[1]


reload(sys)
sys.setdefaultencoding('utf8') # 设置编码


url = 'http://baike.baidu.com/starrank?fr=lemmaxianhua'

def get_content(url):
	driver = webdriver.Chrome('/usr/local/Cellar/chromedriver/2.20/bin/chromedriver') # 创建一个driver用于打开网页，记得找到brew安装的chromedriver的位置，在创建driver的时候指定这个位置
	driver.get(url) # 打开网页
	name_counter = 1
	page = 0;
	while page < 50: # 共50页，这里是手工指定的
		soup = BeautifulSoup(driver.page_source, "html.parser")
		current_names = soup.select('div.ranking-table') # 选择器用ranking-table css class，可以取出包含本周、上周的两个table的div标签
		for current_name_list in current_names:
			# print current_name_list['data-cat']
			if current_name_list['data-cat'] == 'thisWeek': # 这次我只想抓取本周，如果想抓上周，改一下这里为lastWeek即可
				names = current_name_list.select('td.star-name > a') # beautifulsoup选择器语法
				counter = 0;
				for star_name in names:
					counter = counter + 1;
					print star_name.text # 明星的名字是a标签里面的文本，虽然a标签下面除了文本还有一个与文本同级别的img标签，但是.text输出的只是文本而已
					name_counter = name_counter + 1;
		driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click() # selenium的xpath用法，找到包含“下一页”的a标签去点击
		page = page + 1
		time.sleep(2) # 睡2秒让网页加载完再去读它的html代码

	print name_counter # 共爬取得明星的名字数量
	driver.quit()


if __name__=="__main__":
	get_content(url)
