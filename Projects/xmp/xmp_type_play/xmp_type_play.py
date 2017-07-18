#!/usr/bin/env python
#encoding=utf8

import MySQLdb
import os
import sys
import urllib2,cookielib
import json
import hues
from datetime import date,datetime, timedelta

g_tool_hive="/usr/local/complat/cdh5.10.0/hive/bin/hive"

curdir=os.getcwd()
datapath=curdir.replace("/bin","/data")
if not os.path.exists(datapath):
	os.makedirs(datapath)

g_top_num = 20


'''
	片库按类型播放统计
'''
class XMPTypePlay():
	def __init__(self):
		self.kankan_play = '%s/peerid_play_table_%s' %(datapath,date)
		self.jingpin_play = '%s/peerid_conv_table_%s' %(datapath,date)
		self.conn = MySQLdb.connect(host="localhost", user="root", passwd="hive")
		self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
		self.cur.execute('set names utf8')
		self.headers ={
				"Host":"media.v.xunlei.com",
				"Referer": "http://media.v.xunlei.com",
				"cookie":"client=pc;version=5.1.0.3054"
		}
		self.opener = urllib2.build_opener()
		self.play_list=[]
		self.g_map_kkid = {}

	# 导出数据到中间表
	def get_play_movieid_list(self):
		cmd = "%s -e \"use xmp_odl;select fpeerid, fmovieid, ftitle from t_stat_play where ds='%s' and fplay_type=2 and length(fmovieid)>4\">%s" %(g_tool_hive,date, self.kankan_play)
		print cmd
		ret = os.system(cmd)
		if ret != 0:
			print "error:get_play_movieid_list from t_stat_play failed! ret:",ret
			return None

		cmd = "%s -e \"use xmp_odl;select fu1, fu4, '' from xmpconv where ds='%s' and fu3='XMP-JingPin' and length(fu4)>4\">%s" %(g_tool_hive,date, self.jingpin_play)
		print cmd
		ret = os.system(cmd)
		if ret != 0:
			print "error:get_play_movieid_list from xmpconv failed! ret:",ret
			return None

		print "load mysql, return list"

		mid_table = 'pgv_stat_mid.xmp_play_movieid_title'
		self.cur.execute("delete from %s;" %(mid_table))
		self.cur.execute("load data local infile '%s' into table %s" %(self.kankan_play, mid_table))
		self.cur.execute("load data local infile '%s' into table %s" %(self.jingpin_play, mid_table))
		self.cur.execute("select movieid, title, count(*) as pv, count(distinct peerid) as vv from %s group by movieid order by vv desc limit 500" %(mid_table))
		self.play_list = self.cur.fetchall()

	# 构造kankan_id和movieid的映射关系
	def get_info_from_media_lib(self):
		request = urllib2.Request('http://media.v.xunlei.com/pc/id_mapping?media_type=|tv|anime|teleplay|movie', None)
		try:
			resp = self.opener.open(request, None, 40)
			result = resp.read().decode('utf8')
			s = json.loads(result)
			for one in s:
				kankan_id_info = {}
				kankan_id_info['movieid'] = one['movieid']
				kankan_id_info['type'] = one['type']
				self.g_map_kkid[one['kankan_id']] = kankan_id_info
			return True
		except Exception,e:
			print "except Exception e:%s" %(str(e))
			return False

	#　获取topplay
	def get_top_list(self):
		top_list = {}
		kankan_list = {}
		kankan_index = 1	#排行序号
		tv_list = {}
		tv_index = 1
		anime_list = {}
		anime_index = 1
		teleplay_list = {}
		teleplay_index = 1
		movie_list = {}
		movie_index = 1

		cnt = 0
		for one in self.play_list:
			movieid = one['movieid']
			title = one['title']
			pv = one['pv']
			vv = one['vv']
			if 5 == len(movieid):					#kankan_id
				if not self.g_map_kkid.has_key(movieid):
					continue
					if g_top_num < kankan_index:
						continue
					movie_info = {}
					movie_info['movieid']=movieid
					movie_info['title']=title
					movie_info['type']='unknow'
					movie_info['pv']=pv
					movie_info['vv']=vv
					kankan_list[movieid] = movie_info
					kankan_index = kankan_index + 1
					continue
				movieid = g_map_kkid[movieid]['movieid']
			elif 8 == len(movieid) and '4' == movieid[0:1]:		#kankan_vip_id
				if not g_map_kkid.has_key(movieid[3:8]):
					continue
					if g_top_num < kankan_index:
						continue
					movie_info = {}
					movie_info['movieid']=movieid
					movie_info['title']=title
					movie_info['type']='unknow'
					movie_info['pv']=pv
					movie_info['vv']=vv
					kankan_list[movieid] = movie_info
					kankan_index = kankan_index + 1
					continue
				movieid = g_map_kkid[movieid[3:8]]['movieid']
			else:							#media_id
				movieid = 'mi' + movieid

			try:
				#print "after media movieid:", movieid
				http_req = 'http://media.v.xunlei.com/pc/info?movieid=%s' %(movieid)
				#print http_req
				request = urllib2.Request(http_req, None, self.headers)
				resp = self.opener.open(request, None, 40)
				result = resp.read().decode('utf8')
				#print result
				s = json.loads(result)
				title = s['title']
				type = s['type']
				if 'tv' == type:
					if tv_list.has_key(movieid):	#合并看看id翻译过之后的数据
						tv_list[movieid]['pv'] = tv_list[movieid]['pv'] + pv
						tv_list[movieid]['vv'] = tv_list[movieid]['vv'] + vv
						continue
					if g_top_num < tv_index:
						continue
					movie_info = {}
					movie_info['movieid']=movieid
					movie_info['title']=title
					movie_info['type']=type
					movie_info['pv']=pv
					movie_info['vv']=vv
					tv_list[movieid] = movie_info
					tv_index = tv_index + 1
				elif 'anime' == type:
					if anime_list.has_key(movieid):	#合并看看id翻译过之后的数据
						anime_list[movieid]['pv'] = anime_list[movieid]['pv'] + pv
						anime_list[movieid]['vv'] = anime_list[movieid]['vv'] + vv
						continue
					if g_top_num < anime_index:
						continue
					movie_info = {}
					movie_info['movieid']=movieid
					movie_info['title']=title
					movie_info['type']=type
					movie_info['pv']=pv
					movie_info['vv']=vv
					anime_list[movieid] = movie_info
					anime_index = anime_index + 1
				elif 'teleplay' == type:
					if teleplay_list.has_key(movieid):	#合并看看id翻译过之后的数据
						teleplay_list[movieid]['pv'] = teleplay_list[movieid]['pv'] + pv
						teleplay_list[movieid]['vv'] = teleplay_list[movieid]['vv'] + vv
						continue
					if g_top_num < teleplay_index:
						continue
					movie_info = {}
					movie_info['movieid']=movieid
					movie_info['title']=title
					movie_info['type']=type
					movie_info['pv']=pv
					movie_info['vv']=vv
					teleplay_list[movieid] = movie_info
					teleplay_index = teleplay_index + 1
				elif 'movie' == type:
					if movie_list.has_key(movieid):	#合并看看id翻译过之后的数据
						movie_list[movieid]['pv'] = movie_list[movieid]['pv'] + pv
						movie_list[movieid]['vv'] = movie_list[movieid]['vv'] + vv
						continue
					if g_top_num < movie_index:
						continue
					movie_info = {}
					movie_info['movieid']=movieid
					movie_info['title']=title
					movie_info['type']=type
					movie_info['pv']=pv
					movie_info['vv']=vv
					movie_list[movieid] = movie_info
					movie_index = movie_index + 1
				#print "kankan_index:", kankan_index, " tv_index:", tv_index, "anime_index:", anime_index, " teleplay_index:", teleplay_index
				if g_top_num < tv_index and g_top_num < anime_index and g_top_num < teleplay_index and g_top_num < movie_index:
					break
			except Exception,e:
				print "except Exception e:%s" %(str(e)), " movieid=", movieid
				continue

		#top_list["kankan"] = kankan_list
		top_list["movie"] = movie_list
		top_list["tv"] = tv_list
		top_list["anime"] = anime_list
		top_list["teleplay"] = teleplay_list

		return top_list
		encoder = json.dumps(top_list)
		print encoder

	def order_by_vv(self,toplist):
		table = 'pgv_stat.xmp_play_ranking'
		self.cur.execute("delete from %s where date='%s';" %(table, date))
		mid_table = 'pgv_stat_mid.xmp_play_top_order'
		self.cur.execute("create table if not exists %s(movieid varchar(11), vv int)" %(mid_table))

		print 'teleplay_____________________________________'
		keys = top_list["teleplay"].keys()
		self.cur.execute("delete from %s" %(mid_table))
		sql = "insert into %s(movieid, vv) values('defautl', 0)" %(mid_table)
		for key in keys:
			info = top_list["teleplay"][key]
			value = ", ('%s', %d)" %(info['movieid'], info['vv'])
			sql = sql + value
		#print sql
		self.cur.execute(sql)
		self.cur.execute("select movieid from %s order by vv desc limit %d" %(mid_table, len(keys)))
		list = self.cur.fetchall()
		ranking = 1
		for one in list:
			info = top_list["teleplay"][one['movieid']]
			sql = "insert into %s(date, type, ranking, movieid, title, pv, vv) values('%s', '%s', %d, '%s', '%s', %d, %d)" %(table, date, u'电视剧', ranking, info['movieid'], info['title'], info['pv'], info['vv'])
			#print sql
			self.cur.execute(sql.encode('utf8'))
			ranking = ranking + 1

		print 'anime_____________________________________'
		keys = top_list["anime"].keys()
		self.cur.execute("delete from %s" %(mid_table))
		sql = "insert into %s(movieid, vv) values('defautl', 0)" %(mid_table)
		for key in keys:
			info = top_list["anime"][key]
			value = ", ('%s', %d)" %(info['movieid'], info['vv'])
			sql = sql + value
		#print sql
		self.cur.execute(sql)
		self.cur.execute("select movieid from %s order by vv desc limit %d" %(mid_table, len(keys)))
		list = self.cur.fetchall()
		ranking = 1
		for one in list:
			info = top_list["anime"][one['movieid']]
			sql = "insert into %s(date, type, ranking, movieid, title, pv, vv) values('%s', '%s', %d, '%s', '%s', %d, %d)" %(table, date, u'动漫', ranking, info['movieid'], info['title'], info['pv'], info['vv'])
			#print sql
			self.cur.execute(sql.encode('utf8'))
			ranking = ranking + 1

		print 'tv_____________________________________'
		keys = top_list["tv"].keys()
		self.cur.execute("delete from %s" %(mid_table))
		sql = "insert into %s(movieid, vv) values('defautl', 0)" %(mid_table)
		for key in keys:
			info = top_list["tv"][key]
			value = ", ('%s', %d)" %(info['movieid'], info['vv'])
			sql = sql + value
		#print sql
		self.cur.execute(sql)
		self.cur.execute("select movieid from %s order by vv desc limit %d" %(mid_table, len(keys)))
		list = self.cur.fetchall()
		ranking = 1
		for one in list:
			info = top_list["tv"][one['movieid']]
			sql = "insert into %s(date, type, ranking, movieid, title, pv, vv) values('%s', '%s', %d, '%s', '%s', %d, %d)" %(table, date, u'综艺', ranking, info['movieid'], info['title'], info['pv'], info['vv'])
			#print sql
			self.cur.execute(sql.encode('utf8'))
			ranking = ranking + 1

		print 'movie_____________________________________'
		keys = top_list["movie"].keys()
		self.cur.execute("delete from %s" %(mid_table))
		sql = "insert into %s(movieid, vv) values('defautl', 0)" %(mid_table)
		for key in keys:
			info = top_list["movie"][key]
			value = ", ('%s', %d)" %(info['movieid'], info['vv'])
			sql = sql + value
		#print sql
		self.cur.execute(sql)
		self.cur.execute("select movieid from %s order by vv desc limit %d" %(mid_table, len(keys)))
		list = self.cur.fetchall()
		ranking = 1
		for one in list:
			info = top_list["movie"][one['movieid']]
			sql = "insert into %s(date, type, ranking, movieid, title, pv, vv) values('%s', '%s', %d, '%s', '%s', %d, %d)" %(table, date, u'电影', ranking, info['movieid'], info['title'], info['pv'], info['vv'])
			#print sql
			self.cur.execute(sql.encode('utf8'))
			ranking = ranking + 1


# 测试入口
if __name__ == "__main__":
	if len(sys.argv) < 2 :
		yesterday = date.today() - timedelta(days=1)
		date = '%04d%02d%02d' %(yesterday.year, yesterday.month, yesterday.day)
	else:
		date = sys.argv[1]


	xtp=XMPTypePlay()
	#获取看看id和媒资库id的映射关系
	xtp.get_info_from_media_lib()

	#根据播放人数获取排行前500条记录
	xtp.get_play_movieid_list()

	#计算排行版
	top_list = xtp.get_top_list()
	if 0 == len(top_list):
		hues.error("获取top_play_list失败")
		exit

	#重新排序，因为合入看看id翻译之后的id，固顺序可能被打乱
	xtp.order_by_vv(top_list)






