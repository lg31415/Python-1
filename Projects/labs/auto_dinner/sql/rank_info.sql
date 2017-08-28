/*
Navicat SQLite Data Transfer

Source Server         : dinner
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2017-08-28 10:47:53
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for rank_info
-- ----------------------------
DROP TABLE IF EXISTS "main"."rank_info";
CREATE TABLE "rank_info" (
"date"  varchar(10),
"rank"  INTEGER,
"rest_name"  varchar(20),
"dish_name"  varchar(100),
"dish_taste"  varchar(20),
"like_num"  INTEGER,
"ts"  datetime
);
