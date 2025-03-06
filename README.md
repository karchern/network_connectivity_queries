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

- Use `download_networks.sh bvu` to query `bvu` networks from KEGG (can take a few minutes, download is slow...)
  - Make sure to populate `network_ids_to_operate_on.txt` (go to the [KEGG pathway maps URL](https://www.genome.jp/kegg-bin/show_organism?menu_type=pathway_maps&org=bvu) and copy the info into the txt file)
  - Please note: At least for `bvu`, the `Global and overview maps` networks are formatted differently, and right now are not supported by this workflow (should need arise in the future it should not be too hard to make it work).
- Open cytoscape and import networks
  - Run `print_cytoscape_commands.sh` to generate `run_me_with_command_run.txts`
  - Open Cytoscape and execute `command run file="/Users/karcher/network_connectivity_queries/run_me_with_command_run.txt` in the Cytoscape command line to load and prune networks
  - Save session under `session.cys`
- Run `export_networks_to_graphml.py` (by default tries to load `session.cys`)
- Configure `ko_metabolite_map.csv`
- Run `bash query_network.sh` 