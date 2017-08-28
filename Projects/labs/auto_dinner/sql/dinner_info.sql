/*
Navicat SQLite Data Transfer

Source Server         : dinner
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2017-08-28 10:47:28
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for dinner_info
-- ----------------------------
DROP TABLE IF EXISTS "main"."dinner_info";
CREATE TABLE dinner_info(date varchar(10),rest varchar(20),menu varchar(100),insert_time datetime);
