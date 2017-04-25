## URL解析程序

不带中文的解析

描述：

```html
http%3A%2F%2Flist.v.xunlei.com%2Fv%2Ctype%2Cgenre%2Carea%2F5%2Canime%2Crx%2C8%2Fpage3%2F%3Fsfrom%3Dxl9_index

#解析为
http://list.v.xunlei.com/v,type,genre,area/5,anime,rx,8/page3/?sfrom=xl9_index
```

占位：

```
http%3A%2F%2Fmfwz.login.xunlei.xiyou-g.com%2F113.html%3Fsid%3D113%26uid%3Dxlmfwz0007240617%26fcm%3D1%26exts%3D%26time%3D1478520011%26platform%3Dxunlei%26sign%3D18e04cd13262b423da4596b29d00e

# 解析为
http://mfwz.login.xunlei.xiyou-g.com/113.html?sid=113&uid=xlmfwz0007240617&fcm=1&exts=&time=1478520011&platform=xunlei&sign=18e04cd13262b423da4596b29d00e
```

带中文的解析

```html
http%3A%2F%2F48.fans.xunlei.com%2Fcatalog%2Fcatalog.shtml%3Ftype%3D%E6%BC%94%E5%94%B1%E4%BC%9A

#解析为(hive的urldeocde结果)
http://48.fans.xunlei.com/catalog/catalog.shtml?type=演唱会


//怎么会有多上报的%25N呢
http%3A%2F%2F48.fans.xunlei.com%2Fcatalog%2Fcatalog.shtml%3Ftype%3D%25E9%259F%25B3%25E4%25B9%2590
 
# 解析为(hive的urldeocde结果)
http://48.fans.xunlei.com/catalog/catalog.shtml?type=%E9%9F%B3%E4%B9%90

```



## 参考

