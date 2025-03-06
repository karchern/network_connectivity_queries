# Summary

Workflow to query the connectivity of KOs and metabolites based on KEGG

# Requirements
- Cytoscape
- parallel
- python with dependencies (all installable via pip)
  - networkx
  - click
  - csv
  - py4cytoscape

# Download + preprocessing of KEGG reference pathways

### Note

All steps in this section are preprocessing steps to download, modify and export KEGG pathways in python-readable format. As such, these only need to be run once. After step 5, you should find `graphml` networks in the `networks_graphml` folder, which represent the startin point of the analysis

1. `cd aux_scripts`
2. Use `download_networks.sh bvu` to query `bvu` networks from KEGG (can take a few minutes, download is slow...) and put them into the `networks` folder as `.xml` files
  - Make sure to populate `network_ids_to_operate_on.txt` (go to the [KEGG pathway maps URL](https://www.genome.jp/kegg-bin/show_organism?menu_type=pathway_maps&org=bvu) and copy the info into the txt file)
  - Please note: At least for `bvu`, the `Global and overview maps` networks are formatted differently, and right now are not supported by this workflow (should need arise in the future it should not be too hard to make it work).
<!-- 3. Open cytoscape and import networks
  - Run `bash print_cytoscape_commands.sh` to generate `run_me_with_command_run.txt`
  - Open Cytoscape and execute `command run file="/Users/karcher/network_connectivity_queries/run_me_with_command_run.txt` in the Cytoscape command line to load and prune networks (might take a few minutes depending on the number of networks you have downloaded - don't try to close cytoscape)
  - Save session under `session.cys` -->
1. Run `bash print_cytoscape_commands.sh` to generate `fill cytoscape_command_files`. Then run `bash export_networks.sh` to populate `cytoscape_session_files`
2. `cd ..`
3. Run `network_queries/prepare_networks.py export-sessions-to-graphml` (by default tries to load all files in `cytoscape_session_files`, if you want to load another session `--session_file path_to_session_file`)
   
  
- Configure `ko_metabolite_map.csv`
- Run `bash query_network.sh` 