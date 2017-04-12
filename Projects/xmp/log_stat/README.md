## nginx日志统计项目

[TOC]

### barrage_log[弹幕日志统计]

日志格式

```nginx
#183.11.117.147 - - [21/Dec/2016:14:13:02 +0800] "GET /info?type=local&key=D3D77CA263B27157EC6FF4AF0F0431B1A24A715D&subkey=1399749052&duration=1422380&md5=612183a0ebe2520c86aee4837c78b119 HTTP/1.1" 200 20 "-" "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"
```

进度

已结项

### snh48_log[snh48日志统计]

日志格式

```nginx
log_format  mylog  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"'
                      '"$request_time" "$upstream_response_time"';

#219.133.170.82 - - [20/Mar/2017:17:48:04 +0800] "GET /editUserInfo?userID=1234&openID=1234&name=hah1213123123a&sex=1&headImg=headImg HTTP/1.1" 200 21 "-" "Python-urllib/2.7"
```

进度

>2017年4月11日

因为日志的格式并没有改变，所以直接套用以前的程序