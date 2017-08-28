/*
Navicat SQLite Data Transfer

Source Server         : dinner
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2017-08-28 10:47:41
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for history_info
-- ----------------------------
DROP TABLE IF EXISTS "main"."history_info";
CREATE TABLE "history_info" (
"dinner_num"  INTEGER,
"dinner_area"  varchar(20),
"dinner_rest"  varchar(20),
"dinner_dish"  varchar(100),
"dinner_time"  datetime,
"ts"  datetime
);
