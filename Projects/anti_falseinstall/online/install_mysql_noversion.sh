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


# 统计结果数据入中间表
function stat_install()
{
	${MYSQL} -e "use test;set names 'utf8';delete from test.xmp_install_mid where date='${date}';"        # 中间表数据清空
	${MYSQL} -e "use test;set names 'utf8';delete from test.xmp_install where date='${date}';"          # 结果表数据清空

	for flag in 'normal' 'decrypt';do
		echo -e "\e[031m===$flag=====\e[0m"
		# 加载数据
		${MYSQL} -e "set names 'utf8';load data local infile '$datapath/${flag}_install_${date}' into table test.xmp_install_mid;"

		# new
		sql="use test;select date,package_name,' ',count(*),count(distinct peerid),'00','$flag' from xmp_install_mid where date='${date}' and installtype='00' and flag='$flag' group by date,package_name;"
		echo $sql
		${MYSQL} -e "$sql" > $datapath/new.${flag}.${date}

		# old
		sql="use test;select date,package_name,' ', count(*),count(distinct peerid),'01','$flag' from xmp_install_mid where date='${date}' and installtype='01' and flag='$flag' group by date,package_name;"
		echo $sql
		${MYSQL} -e "$sql" > $datapath/old.${flag}.${date}

		# silence
		sql="use test;select date,package_name,' ',count(*),count(distinct peerid),'10','$flag' from xmp_install_mid where date='${date}' and installtype='10' and flag='$flag' group by date,package_name;"
		echo $sql
		${MYSQL} -e "$sql" > $datapath/silence.${flag}.${date}

		# unsilence
		sql="use test;select date,package_name,' ',count(*),count(distinct peerid),'11','$flag' from xmp_install_mid where date='${date}' and installtype='11' and flag='$flag' group by date,package_name;"
		echo $sql
		${MYSQL} -e "$sql" > $datapath/unsilence.${flag}.${date}

		# uninstall
		# ${MYSQL10} -e "use test;select date,package_name,version,count(*),count(distinct peerid),'uninstall','$flag' from xmp_install_mid where date='${date}' and install%10=0 and flag='$flag' group by date,package_name,version" > $datapath/uninstall.${flag}.${date}

		# 导入结果数据
		#ls $datapath/*${flag}.${date}
		cat $datapath/*${flag}.${date} > $datapath/install_${flag}_${date}
		mkdir $datapath/tmp && mv $datapath/*${flag}.${date} $datapath/tmp
		${MYSQL} -e "use test;set names 'utf8';load data local infile '$datapath/install_${flag}_${date}' into table test.xmp_install;"

	done
}

# 统计所有安装
function diff_install()
{
	sel="date,channel,installtype,pv,uv"
	tblb="select $sel from test.xmp_install where date=$date and flag='decrypt'"
	tbla="select $sel from test.xmp_install where date=$date and flag='normal'"
	sql="use test;select a.date,a.channel,a.installtype,a.pv,b.pv,a.pv-b.pv as 'normal.pv-decrpt.pv',a.uv,b.uv,a.uv-b.uv as 'normal.uv-decrpt.uv' from ($tbla) a inner join ($tblb) b on a.date=b.date and a.channel=b.channel and a.installtype=b.installtype;"
	echo $sql
	${MYSQL} -e "use test;$sql">diff_install_$date
	# 原始方法有问题
	# sed -i '1i 日期\t渠道\t安装类型\t正常安装次数(A)\t加密安装次数(B)\tA-B\t正常安装人数(C)\t加密安装人数(D)\tC-D' diff_install_$date
	# sed -i -e 's/\b00\b/全新无界面/' -e 's/\b01\b/覆盖无界面/' -e 's/\b10\b/全新有界面/' -e 's/\b11\b/覆盖有界面/' diff_install_$date

	# 新方法
	awk '{if($3=="00") $3="全新无界面";else if($3=="01") $3="覆盖无界面";else if($3=="10") $3="全新有界面";else if($3=="11") $3="覆盖有界面";else $3="Error"; print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8"\t"$9}' diff_install_$date >diff_install_cov_$date
	sed -i '1i 日期\t渠道\t安装类型\t正常安装次数(A)\t加密安装次数(B)\tA-B\t正常安装人数(C)\t加密安装人数(D)\tC-D' diff_install_cov_$date

	rm -f diff_install_$date
}

# 只统计新装
function diff_install_new()
{
    sel="date,channel,sum(pv) as spv,sum(uv) as suv"
	tblb="select $sel from test.xmp_install where date=$date and flag='decrypt' and installtype in ('00','10') group by date,channel"
	tbla="select $sel from test.xmp_install where date=$date and flag='normal' and installtype in ('00','10') group by date,channel"
	sql="use test;select a.date,a.channel,'新装',a.spv,b.spv,a.spv-b.spv,a.suv,b.suv,a.suv-b.suv from ($tbla) a inner join ($tblb) b on a.date=b.date and a.channel=b.channel;"
	echo $sql
	${MYSQL} -e "use test;$sql">>diff_install_cov_$date
}



# 程序入口
stat_install
# diff_install
diff_install_new


cd -
exit 0

