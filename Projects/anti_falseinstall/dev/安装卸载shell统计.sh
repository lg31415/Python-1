#!/bin/bash

sql="create table if not exists test.xmp_install(date varchar(8),package_name varchar(255),version varchar(255),installtype varchar(10),install int,count int);"

# 全字段
# 1	  2	 3	     4		5	6	7		8		9			10		11	12		13	     14		15	      16  17
# install,peerid,installtype,newinstall,version,firstinstallsource,lastinstallsource,firstinstallversion,lastuninstalltime,channel,firstinstaltime,installtime,package_name,fatherprocessname,fip,ftime

#{1: 'install',
# 2: 'peerid',
# 3: 'installtype',
# 4: 'newinstall',
# 5: 'version',
# 6: 'firstinstallsource',
# 7: 'lastinstallsource',
# 8: 'firstinstallversion',
# 9: 'lastuninstalltime',
# 10: 'channel',
# 11: 'firstinstaltime',
# 12: 'installtime',
# 13: 'package_name',
# 14: 'fatherprocessname',
# 15: 'fip',
# 16: 'ftime'}


# 真正使用到字段（老定义）
package_name,version,installtype,install

# 真正使用到的字段（新定义）
package_name,version,installtype,install,newinstall

# awk分组统计(package_name,version,installtype,install)
awk '{print $13"\t"$5"\t"$3"\t"$1}'|uniq -c


### uniq计数法
# new
awk '/$3==00/{if($3==00 && $1~/08$/) print $13"\t"$5"\t"$3"\t"$1}'|uniq -c

# old
awk '/$3==01/{if($3==01 && $1~/08$/) print $13"\t"$5"\t"$3"\t"$1}'|uniq -c

# silence
awk '/$3==10/{if($3==10 && $1~/08$/) print $13"\t"$5"\t"$3"\t"$1}'|uniq -c

# unsilence
awk '/$3==11/{if($3==11 && $1~/08$/) print $13"\t"$5"\t"$3"\t"$1}'|uniq -c

# uninstall
awk '{if(install>2399 && install%10=0) print $13"\t"$5"\t"$3"\t"$1}'|uniq -c

### 数组运算法
awk '{if($3==00 && $1~/8$/) a[$13"\t"$5"\t"$3"\t"$1]+=1}END{ for(i in a) print i"\t"a[i]}'