#!/bin/bash -e
set -euo pipefail

base="bvu"
while read line
do
	networkid=$(echo $line | awk '{print $1}')
	# Save the rest of the white space delimited lines as networkname
	networkname=$(echo $line | awk '{for(i=2;i<=NF;++i)printf "%s ", $i; print ""}')
	echo -e "network import file file=\"$(pwd)/networks/${base}${networkid}.xml\""
	echo -e "network delete network=\"${networkname} [${base}${networkid}]\" nodeList=KEGG_NODE_TYPE:map"
done < network_ids_to_operate_on.txt > run_me_with_command_run.txt


