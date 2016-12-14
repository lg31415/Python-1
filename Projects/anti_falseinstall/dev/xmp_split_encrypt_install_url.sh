#!/bin/bash
dir=`dirname $0` && dir=`cd $dir && pwd`
source /usr/local/sandai/server/bin/common/global_var.sh
cd $dir

datapath=${dir/\/bin/\/data}
mkdir -p $datapath

if [ ${#@} -eq 1 ];then
	date=$1
else
	date=`date -d 'yesterday' "+%Y%m%d"`
fi


hql="${UDFLIB};${UDF_CREATE};
add file t_stat_url_upload_split_mapper.py;
select transform(*)
using 't_stat_url_upload_split_mapper.py'
as install,peerid,installtype,newinstall,version,firstinstallsource,lastinstallsource,firstinstallversion,lastuninstalltime,channel,firstinstaltime,installtime,package_name,fatherprocessname,fip,ftime
from(select fu1 as peerid,fu5 as encrypt_url from xmp_odl.xmpconv where ds='$date' and fu3='XS-Stat')a"

echo $hql
${HIVE} -e "$hql">anti_install_$date


cd -
exit 0



