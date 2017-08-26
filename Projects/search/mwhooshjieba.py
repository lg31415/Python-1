#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:利用whoosh和jieba实现全文检索
	Ref:http://www.jeyzhang.com/realization-of-full-chinese-text-search-using-whoosh-and-jieba.html
	Date:2016/9/19
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

import hues
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import json

def msearch():
    # 使用结巴中文分词
	analyzer = ChineseAnalyzer()

	# 创建schema, stored为True表示能够被检索
	schema = Schema(title=TEXT(stored=True, analyzer=analyzer), path=ID(stored=False),content=TEXT(stored=True, analyzer=analyzer))

	# 存储schema信息至'indexdir'目录下
	indexdir = 'data/'
	if not os.path.exists(indexdir):
		os.mkdir(indexdir)
	ix = create_in(indexdir, schema)

	# 按照schema定义信息，增加需要建立索引的文档（注意：字符串格式需要为unicode格式）
	# 如何快速将文件内容进行索引，或者说是增量索引，这个是实用的关键（比不上elasticsearch)
	writer = ix.writer()
	writer.add_document(title=u"第一篇文档", path=u"/a",	content=u"这是我们增加的第一篇文档")
	writer.add_document(title=u"第二作文", path=u"/b", content=u"第二篇文档也很interesting！")
	writer.add_document(title=u"这篇文档非常没意思", path=u"/b", content=u"第二篇文档也很interesting！")
	writer.commit()

	# 创建一个检索器
	searcher = ix.searcher()

	# 检索标题中出现'文档'的文档
	results = searcher.find("title", u"文档")  #简单的查询（后面可以近一步的扩展）

	# 检索出来的每个结果，数据格式为dict{'title':.., 'content':...}
	for i,result in enumerate(results):
		hues.info("检索出的第%s篇文档: title:%s\t,bm25得分:%s" %(i,result['title'],result.score))
		firstdoc = result.fields()
		jsondoc = json.dumps(firstdoc, ensure_ascii=False)  # python2中，需要使用json来打印包含unicode的dict内容
		print jsondoc										# 打印出检索出的文档全部内容
		print "关键词高亮:",result.highlights("title")					# 高亮标题中的检索词 <b class="match term0">文档</b>



if __name__ == "__main__":
    msearch()

