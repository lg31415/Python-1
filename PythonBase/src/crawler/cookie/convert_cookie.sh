#!/bin/bash
cd $(dirname $0)
if [ $# != 2 ];then
	echo "parameters wrong"
	exit 1
fi

input=$1
output=$2

awk '{if($5~/[0-9]+/) print $1"\t"$2"\t"$3"\t"$4"\t\t"$6"\t"$7;else print  $1"\t"$2"\t"$3"\t"$4"\t\t"$5"\t"$6 }' $input > $output

sed -i '1i# Netscape HTTP Cookie File' $output
sed -i '2i# http://curl.haxx.se/rfc/cookie_spec.html' $output
sed -i '3i# This is a generated file!  Do not edit.' $output
sed -i '4i\\n' $output

exit 0
