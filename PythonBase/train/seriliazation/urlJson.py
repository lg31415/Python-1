# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：获取网页内容，Python解析json格式的文件，统计输出结果
  输出结果的格式如下：
  {kankan_id:[{type:'teleplay',movieid:'mi1014597'},...,{type:'teleplay',movieid:'mi1014597'}],
   kankan_id:[{type:'teleplay',movieid:'mi1014597'},...,{type:'teleplay',movieid:'mi1014597'}],
   kankan_id:[{type:'teleplay',movieid:'mi1014597'},...,{type:'teleplay',movieid:'mi1014597'}],
   kankan_id:[{type:'teleplay',movieid:'mi1014597'},...,{type:'teleplay',movieid:'mi1014597'}]
  }
'''

import urllib2
import json
from collections import OrderedDict  #保证字典的按顺序解析

def run(url):
    results_dict={}
    src_url=urllib2.urlopen(url)
    src_content=src_url.read()
    #src_json=json.dumps(src_python)     #将python列表转化为json对象
    #print repr(src_python)
    #print(src_json)
    src_python=json.loads(src_content)
    print('json反解析的数据格式类型是：',type(src_python))  #存在编码转化问题,此时json已经将原始的字符串转化为python的列表形式了
    for one_d in src_python:
        #print(one_d)
        if one_d[u'kankan_id']!=u"":
            if results_dict.get(one_d[u'kankan_id']): #如果已经存在该kankan_id,kankan_id不唯一
                 results_dict[one_d[u'kankan_id']]=results_dict.get(one_d[u'kankan_id']).append({'movieid':one_d['movieid'],'type':one_d['type']}) #字典内部键值对的赋值
            else:
                 results_dict[one_d[u'kankan_id']]=[{'movieid':one_d['movieid'],'type':one_d['type']}]; #若不存在则之间赋值
    return  results_dict;

def urlParase(url):
    resDict={}
    resonse=urllib2.urlopen(url)
    content=resonse.read()
    plist=json.loads(content) #解析后得到的列表，先转换一下
    for item in plist:
        kankan_id=item['kankan_id']
        if kankan_id!="":
            resDict[kankan_id]={'type':item['type'],'movieid':item['movieid']}
    return resDict

# url解析程序的主入口
def urlmain():
    url='http://media.v.xunlei.com/pc/id_mapping?media_type=|tv|anime|teleplay|movie'
    #resDict=run(url)
    #print('FinalRes:',resDict)
    #resDict=urlParase(url)
    #print('FinalRes:',resDict)



'''
json的数据类型：
***注意：json的key都要加双引号
1）数值型：123不加引号
2）null:null
3) 布尔型：true,false
4) 数组型：[1,2,3]
5) 字符串型：“hello”
'''
text='''
{
    "retCode": "0000",
    "retMsg": "张三丰",
    "testcolor": "jajjdw",
    "retList":
    {
        "le1": {"price": "4800000", "commId": "56761"},
        "le2": {"price": "4800000", "commId": "56761"}
    }
}
'''

'''
    将形如字典格式的字符串转换成字典
'''
def jsonReadStr():
    str2dict=json.loads(text)
    print str2dict # unicode&str--->utf8
    #print textdict.encode('utf8') # 有误





'''
  在不同的编程语言之间传递对象
'''

def jsonRead():
    #f=open('../data/temp1.json')
    #print 'Content:',f.read()
    f=file('../../data/temp1.json')  #Ref:http://blog.chinaunix.net/uid-9525959-id-3074355.html
    s=json.load(f,object_pairs_hook=OrderedDict)
    print s,type(s)
    f.close()
    print 'KEYS:',s.keys()
    print 'VALUES:',s.values()


def jsonWrite():
    mdict={'ha':1,'di':2,'niw':3}
    f=open('../../data/write.json','w')
    json.dump(mdict,f)
    f.close()

'''
    完整展示json多级文件的读取和写入
'''
def jsonWhole():
    f=file('../../data/document.json')
    s=json.load(f)
    s['mem']
    return s





if __name__ == "__main__":
    #jsonReadStr()
    #jsonRead()
    #jsonWrite()
    jsonWhole()

