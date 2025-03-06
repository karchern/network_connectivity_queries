#!/bin/bash -e

path_to_cytoscape_executable="/Applications/Cytoscape_v3.10.3/cytoscape.sh"
ln -s -f $path_to_cytoscape_executable cytoscape.sh
path_to_jdk="/opt/homebrew/opt/openjdk@17"
rm -f networks_graphml
for file in $(ls cytoscape_command_files)
do
	export JAVA_HOME=${path_to_jdk}; bash cytoscape.sh --script /Users/karcher/network_connectivity_queries/aux_scripts/cytoscape_command_files/${file}
done