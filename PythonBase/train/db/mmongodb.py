#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：mongodb基础学习
'''

import pymongo

def mpymogo():
    con=pymongo.MongoClient('localhost',27017)
    # 选择test数据库
    db=con['test']  # 或者采用db=con.test这种方式
    # 选择users集合
    collection=db.users

    # 添加单挑数据到集合中
    user = {"name":"cui","age":"1"}
    collection.insert(user)

    # 查询db下的所有集合
    print db.collection_names()

    # 查询集合中的所有记录
    for data in collection.find():
        print data


    # 简单参数查询
    for data in collection.find({"name":"cui"}):
        print  '---',data

    # 高级查询(这个查询有问题)
    for data in collection.find({'age':{'$gt':'5'}}):
        print data


if __name__ == "__main__":
    mpymogo()
