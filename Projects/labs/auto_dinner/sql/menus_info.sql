/*
Navicat SQLite Data Transfer

Source Server         : dinner
Source Server Version : 30714
Source Host           : :0

Target Server Type    : SQLite
Target Server Version : 30714
File Encoding         : 65001

Date: 2017-08-28 10:47:47
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for menus_info
-- ----------------------------
DROP TABLE IF EXISTS "main"."menus_info";
CREATE TABLE "menus_info" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"rest_name"  TEXT,
"rest_id"  TEXT,
"dish_name"  TEXT,
"dish_id"  TEXT,
"ts"  datetime
);

-- ----------------------------
-- Indexes structure for table menus_info
-- ----------------------------
CREATE UNIQUE INDEX "main"."rest_dish"
ON "menus_info" ("rest_name" ASC, "dish_name" ASC);
