# Summary

Workflow to query the connectivity of KOs and metabolites based on KEGG

# Requirements
- Cytoscape
- python with dependencies (all installable via pip)
  - networkx
  - click
  - csv
  - py4cytoscape

# Overview

- Use `download_networks.sh` to query networks from KEGG (can take a few minutes, download is slow...)
- Open cytoscape and import networks
  - Run `print_cytoscape_commands.sh` to generate `run_me_with_command_run.txts`
  - Open Cytoscape and execute `command run file="/Users/karcher/network_connectivity_queries/run_me_with_command_run.txt` in the Cytoscape command line to load and prune networks
- Merge networks in Cytoscape and export as `master_network.graphml`. Make sure merge on `KEGG_NODE_LABEL`
- Configure `ko_metabolite_map.csv`
- Run `bash query_network.sh` 