#!/bin/bash -e
set -euo pipefail

rm -f cytoscape_command_files/*

base="eco"
while read line
do
	# Skip the line if it doesnt start with a number (these are comment lines)
    if ! echo "$line" | grep -q '^[0-9]'; then
        continue
    fi	
	networkid=$(echo $line | awk '{print $1}')
	# Save the rest of the white space delimited lines as networkname
	networkname=$(echo $line | awk '{for(i=2;i<=NF;++i)printf "%s ", $i; print ""}')
	echo -e "network import file file=\"$(pwd)/../networks/${base}${networkid}.xml\""
	echo -e "network delete network=\"${networkname} [${base}${networkid}]\" nodeList=KEGG_NODE_TYPE:map"
	echo -e "network export options=\"graphml\" outputFile=\"$(pwd)/../networks_graphml/${base}${networkid}.graphml\""
done < ../network_ids_to_operate_on.txt > cytoscape_command_files/tmp.txt

n=15
cd cytoscape_command_files

# Split tmp.txt into files with n lines
split -l $n tmp.txt split_

# Rename the split files to have a numeric suffix
a=1
for f in split_*
do
    mv "$f" "split_${a}.txt"
    a=$((a + 1))
done

for f in $(ls . | grep txt$ | sed "s/\.txt//")
do
	cat ${f}.txt <(echo -e "session save as file=\"$(pwd)/../cytoscape_session_files/${f}.cys\"\ncommand quit") > a
	mv a ${f}.txt
done

rm -f a
rm -f tmp.txt
cd ..
