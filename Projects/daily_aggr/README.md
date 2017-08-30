##资源聚合
[TOC]

### 数据库设计

collection_resource_info

```mysql
CREATE TABLE `collection_base_info` (
`id`  bigint(20) NOT NULL AUTO_INCREMENT ,
`pageurlhash`  varchar(255)  NOT NULL ,
`pageurl`  varchar(255)  NOT NULL DEFAULT '' ,
`site`  varchar(50)  NULL DEFAULT '' COMMENT '链接的主机域名' ,
`poster`  varchar(255)  NULL DEFAULT NULL ,
`title`  varchar(255)  NOT NULL DEFAULT '' ,
`type`  varchar(32)  NOT NULL DEFAULT '' COMMENT '文章分类' ,
`source`  varchar(30)  NOT NULL DEFAULT '' COMMENT '文章来源' ,
`abstract`  varchar(255)  NOT NULL DEFAULT '' COMMENT '摘要' ,
`tags`  varchar(100)  NOT NULL DEFAULT '' COMMENT '关键词tag' ,
`read_num`  int(10) NULL DEFAULT 0 COMMENT '阅读量' ,
`comment_num`  int(10) NULL DEFAULT 0 COMMENT '评论量' ,
`publish_time`  datetime NULL DEFAULT '0000-00-00 00:00:00' ,
`insert_time`  datetime NULL DEFAULT '0000-00-00 00:00:00' ,
PRIMARY KEY (`id`),
UNIQUE INDEX `source` (`pageurl`, `source`) USING BTREE ,
INDEX `insert_time` (`insert_time`) USING BTREE ,
INDEX `title` (`title`) USING BTREE )
ENGINE=MyISAM DEFAULT CHARSET=utf8;
```

此处只有一个基础信息表，缺失评论表，文章详情表

文章评论信息表

- article_comment_info

```mysql
CREATE TABLE `article_comment_info` (
`id`  bigint(20) NOT NULL AUTO_INCREMENT ,
`pageurlhash`  varchar(255)  NOT NULL ,
`pageurl`  varchar(255)  NOT NULL DEFAULT '' ,
`title`  varchar(255)  NOT NULL DEFAULT '' ,
`read_num`  int(10) NULL DEFAULT 0 COMMENT '阅读量' ,
`comment_num`  int(10) NULL DEFAULT 0 COMMENT '评论量' ,
`publish_time`  datetime NULL DEFAULT '0000-00-00 00:00:00' ,
`insert_time`  datetime NULL DEFAULT '0000-00-00 00:00:00' ,
PRIMARY KEY (`id`),
UNIQUE INDEX `source` (`pageurl`, `source`) USING BTREE ,
INDEX `insert_time` (`insert_time`) USING BTREE ,
INDEX `title` (`title`) USING BTREE )
ENGINE=MyISAM DEFAULT CHARSET=utf8;
```

文章详情表

- article_detail_info

提取url域名：

```mysql
select substring_index(substring_index('http://wz.cnblogs.com/my/search/?q=cookie','/',3),'/',-1);
update collection_base_info set site=substring_index(substring_index(pageurl,'/',3),'/',-1);
```

> MySQL触发器的使用

### 方案设计

#### 非框架版collection_origin

采用手动信息入库的方式，在每个爬虫里都要单独处理浏览器的初始化和信息入库的工作

#### 框架版collection_scrapy

爬虫只负责信息的提取，而信息入库的工作交给管道进行统一处理

 ##参考