# Summary

Workflow to query the connectivity of KOs and metabolites based on KEGG

# Requirements
- Cytoscape (only for preprocessing)
- Rest can be installed via pip: `pip install git+https://github.com/karchern/network_connectivity_queries.git`

# Download + preprocessing of KEGG reference pathways

All steps in this section are preprocessing steps to download, modify and export KEGG pathways in python-readable format. As such, these only need to be run once. After step 3, you should find `graphml` networks in the `networks_graphml` folder, which represent the startin point of the analysis.

For `bvu`, all of these have already been performed, so those networks are ready to be queried.

1. `cd aux_scripts`
2. Use `download_networks.sh bvu` to query `bvu` networks from KEGG (can take a few minutes, download is slow...) and put them into the `networks` folder as `.xml` files
  - Make sure to populate `network_ids_to_operate_on.txt` (go to the [KEGG pathway maps URL](https://www.genome.jp/kegg-bin/show_organism?menu_type=pathway_maps&org=bvu) and copy the info into the txt file)
  - Please note: At least for `bvu`, the `Global and overview maps` networks are formatted differently, and right now are not supported by this workflow (should need arise in the future it should not be too hard to make it work).
3. Run `bash print_cytoscape_commands.sh` to generate `fill cytoscape_command_files`. Then run `bash export_networks.sh` to populate `cytoscape_session_files`
   
# Querying distances between enzymes and metabolites

A core feature of this workflow is to take a set of enzyme <-> metabolite pairs and query their shortest path(s) in KEGG networks. To this end all downloaded and preprocessed KEGG networks (by default located in `networks_graphml`) will be searched, and for each ko <-> metabolite pair and network, a result line will be written

To run

- Configure `ko_metabolite_map.csv` with your pairings of interest. You can add comment lines for readability, which will be ignored by the script.
- `python network_queries/main.py query-shortest-distances --ko_metabolite_csv ko_metabolite_map.csv`
  - Program will issue a warning if a given pairing was _never_ found - this could be because a path does no exist or because either KO or metabolite were misspelt.

# Finding (direct) neighbors of KOs/metabolites

- Configure `seeds.txt`. Should be a 1-column file containing seed nodes. Can be KOs, metabolites, or both.
- To compute sets of immediate neighbors of node entries in `seeds.txt`, run `python network_queries/main.py query-neighborhoods --degree_of_neighborhood 1`. If you want to query more extended neighborhood spaces (i.e neighbors of neighbors, neighbors of neighbors of neighbors etc), increase `--degree_of_neighborhood`
  - Programm will issue a warning should a seed be found in no network.
