##收藏聚合
[TOC]

### 聚合源

| 来源           | 技术方案                                 | 备注          |
| ------------ | ------------------------------------ | ----------- |
| 博客园          | selenium+chrome.driver(cookies)利用浏览器 | 模拟点击，解析html |
| 今日头条         | selenium+chrome.driver(cookies)利用浏览器 | 模拟滚动，解析html |
| 开发者头条        | selenium+chrome.driver(cookies)利用浏览器 | 模拟点击，解析html |
| 推酷           | selenium+chrome.driver(cookies)利用浏览器 | 模拟点击，解析html |
| csdn         | selenium+chrome.driver(cookies)手动载入  | 解析json响应    |
| 简书           | requests+cookies                     | 解析响应的部分html |
| Segmentfault | 有弹窗登录问题，不知道如何解决                      |             |
|              |                                      |             |
|              |                                      |             |

#### 博客园

可以将利用浏览器的cookie进行有界面抓取和解析的部分剥离出来，单独成为一个类

##### 今日头条

##### 开发者头条

##### 推酷

##### csdn

##### 简书

##### Segmentfault

 ##参考