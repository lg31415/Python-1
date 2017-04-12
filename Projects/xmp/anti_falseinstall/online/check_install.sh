#!/bin/bash
dir=`dirname $0` && dir=`cd $dir && pwd`
source /usr/local/sandai/server/bin/common/global_var.sh
cd $dir

#安装核对主程序

datapath="$dir/data/"
mkdir -p $datapath
echo $datapath


if [ ${#@} -eq 1 ];then
	date=$1
else
	date=`date -d 'yesterday' "+%Y%m%d"`
fi

####PART1: 导出反安装的信息
hql="select fu1 as peerid,fu5 as encrypt_url from xmp_odl.xmpconv where ds='$date' and fu3='XS-Stat' order by peerid;"
echo $hql
${HIVE} -e "$hql">$datapath/encrypt_install_$date

# 解密安装信息
python dencrypt_split_url.py $datapath/encrypt_install_$date $datapath/decrypt_install_$date

###PART2: 导出正常安装的信息
hql="select ds,peerid,installtype,newinstall,version,package_name,lastinstallsource,'normal' from xmp_bdl.t_stat_url_upload_split where ds='${date}' and install=2606 order by peerid;"
#hql="select furl from xmp_odl.t_stat_url_upload where ds='${date}';"
echo $hql
${HIVE} -e "$hql">$datapath/normal_install_$date

#安装信息分割
#python normal_split_url.py $datapath/normal_install_$date $datapath/normal_install_$date

### 汇总数据
sh install_mysql_noversion.sh 

cd -
exit 0

