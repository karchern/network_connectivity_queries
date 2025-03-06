#!/bin/bash -e
base=$1
out="../networks/"
mkdir -p $out
while read line
do
	# Skip the line if it doesnt start with a number (these are comment lines)
    if ! echo "$line" | grep -q '^[0-9]'; then
        continue
    fi	
	networkid=$(echo $line | awk '{print $1}')
	networkname=$(echo $line | awk '{print $2}')
	wget http://rest.kegg.jp/get/${base}${networkid}/kgml -O ${out}${base}${networkid}.xml
done < ../network_ids_to_operate_on.txt
