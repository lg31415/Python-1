##资源聚合
[TOC]

### 数据库设计

resource_info

```mysql
CREATE TABLE `collection_base_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pageurlhash` varchar(255) NOT NULL,
  `pageurl` varchar(255) NOT NULL DEFAULT '',
  `title` varchar(255) NOT NULL DEFAULT '',
  `type` varchar(32) NOT NULL DEFAULT '',
  `source` varchar(30) NOT NULL DEFAULT '',
  `abstract` varchar(255) NOT NULL DEFAULT '',
  `tags` varchar(100) NOT NULL DEFAULT '',
  `commment` varchar(255) DEFAULT NULL,
  `publish_time` datetime DEFAULT '0000-00-00 00:00:00',
  `insert_time` datetime DEFAULT '0000-00-00 00:00:00',
  `level` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `source` (`pageurl`,`source`),
  KEY `insert_time` (`insert_time`),
  KEY `title` (`title`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
```





 ##参考