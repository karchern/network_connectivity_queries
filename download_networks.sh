#!/bin/bash -e
base='bvu'
out="networks/"
mkdir -p $out
while read line
do
	networkid=$(echo $line | awk '{print $1}')
	networkname=$(echo $line | awk '{print $2}')
	wget http://rest.kegg.jp/get/${base}${networkid}/kgml -O ${out}${base}${networkid}.xml
done < network_ids_to_operate_on.txt