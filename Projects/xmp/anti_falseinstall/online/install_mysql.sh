#!/bin/bash
dir=`dirname $0` && dir=`cd $dir && pwd`
source /usr/local/sandai/server/bin/common/global_var.sh
cd $dir

date=$1
[ -z $date ]&&date=`date -d"-1day" +%Y%m%d`

datapath="$dir/data"
mkdir datapath
echo $datapath


# 创建相关表
${MYSQL} -e "create table if not exists test.xmp_install_mid(date varchar(10),peerid varchar(25),installtype varchar(10),newinstall int,version varchar(255),package_name varchar(255),lastinstallsource varchar(255),flag varchar(10));"

${MYSQL} -e "create table if not exists test.xmp_install(date varchar(10),channel varchar(255),version varchar(255), pv int,uv int,installtype varchar(10),flag varchar(10));"


# 统计结果数据
function stat_install()
{
	${MYSQL} -e "use test;set names 'utf8';delete from test.xmp_install_mid where date='${date}';"        # 中间表数据清空
	${MYSQL} -e "use test;set names 'utf8';delete from test.xmp_install where date='${date}';"          # 结果表数据清空

	for flag in 'normal' 'decrypt';do
		echo -e "\e[031m===$flag=====\e[0m"
		# 加载数据
		${MYSQL} -e "set names 'utf8';load data local infile '$datapath/${flag}_install_${date}' into table test.xmp_install_mid;"

		# new
		sql="use test;select date,package_name,version,count(*),count(distinct peerid),'00','$flag' from xmp_install_mid where date='${date}' and installtype='00' and flag='$flag' group by date,package_name,version;"
		echo $sql
		${MYSQL} -e "$sql" > $datapath/new.${flag}.${date}

		# old
		sql="use test;select date,package_name,version, count(*),count(distinct peerid),'01','$flag' from xmp_install_mid where date='${date}' and installtype='01' and flag='$flag' group by date,package_name,version;"
		echo $sql
		${MYSQL} -e "$sql" > $datapath/old.${flag}.${date}

		# silence
		sql="use test;select date,package_name,version,count(*),count(distinct peerid),'10','$flag' from xmp_install_mid where date='${date}' and installtype='10' and flag='$flag' group by date,package_name,version;"
		echo $sql
		${MYSQL} -e "$sql" > $datapath/silence.${flag}.${date}

		# unsilence
		sql="use test;select date,package_name,version,count(*),count(distinct peerid),'11','$flag' from xmp_install_mid where date='${date}' and installtype='11' and flag='$flag' group by date,package_name,version;"
		echo $sql
		${MYSQL} -e "$sql" > $datapath/unsilence.${flag}.${date}

		# uninstall
		# ${MYSQL10} -e "use test;select date,package_name,version,count(*),count(distinct peerid),'uninstall','$flag' from xmp_install_mid where date='${date}' and install%10=0 and flag='$flag' group by date,package_name,version" > $datapath/uninstall.${flag}.${date}

		# 导入结果数据
		#ls $datapath/*${flag}.${date}
		cat $datapath/*${flag}.${date} > $datapath/install_${flag}_${date}
		mkdir $datapath/tmp && mv $datapath/*${flag}.${date} $datepath/tmp
		${MYSQL} -e "use test;set names 'utf8';load data local infile '$datapath/install_${flag}_${date}' into table test.xmp_install;"

	done
}

function diff_install()
{
	sel="date,channel,version,pv,uv,installtype,flag"
	tblb="select $sel from test.xmp_install where date=$date and flag='decrypt'"
	tbla="select $sel from test.xmp_install where date=$date and flag='normal'"
	sql="use test;select a.date,a.channel,a.installtype,a.pv-b.pv as 'normal.pv-decrpt.pv',a.uv-b.uv as 'normal.uv-decrpt.uv' from ($tbla) a inner join ($tblb) b on a.date=b.date and a.channel=b.channel and a.installtype=b.installtype;"
	echo $sql
	${MYSQL10} -e "use test;$sql">diff_install_$date

}




# 程序入口
stat_install
diff_install


cd -
exit 0

