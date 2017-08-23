/*
Navicat MySQL Data Transfer

Source Server         : vm_122
Source Server Version : 50630
Source Host           : localhost:3306
Source Database       : media_lib

Target Server Type    : MYSQL
Target Server Version : 50630
File Encoding         : 65001

Date: 2017-08-22 20:18:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for collection_base_info
-- ----------------------------
DROP TABLE IF EXISTS `collection_base_info`;
CREATE TABLE `collection_base_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pageurlhash` varchar(255) NOT NULL,
  `pageurl` varchar(255) NOT NULL DEFAULT '',
  `poster` varchar(255) DEFAULT NULL,
  `title` varchar(255) NOT NULL DEFAULT '',
  `type` varchar(32) NOT NULL DEFAULT '' COMMENT '文章分类',
  `source` varchar(30) NOT NULL DEFAULT '' COMMENT '文章来源',
  `abstract` varchar(255) NOT NULL DEFAULT '' COMMENT '摘要',
  `tags` varchar(100) NOT NULL DEFAULT '' COMMENT '关键词tag',
  `read_num` int(10) DEFAULT '0' COMMENT '阅读量',
  `comment_num` int(10) DEFAULT '0' COMMENT '评论量',
  `publish_time` datetime DEFAULT '0000-00-00 00:00:00',
  `insert_time` datetime DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `source` (`pageurl`,`source`),
  KEY `insert_time` (`insert_time`),
  KEY `title` (`title`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
