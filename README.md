# Summary

Workflow to query the connectivity of KOs and metabolites based on KEGG

# Requirements
- Cytoscape
- python with dependencies
  - networkx
  - matplotlib

# Overview

- Use `download_networks.sh` to query networks from KEGG
- Open cytoscape and import networks
  - Run `print_cytoscape_commands.sh` to generate `import_networks_in_cytoscape.txt` to copy into the cytoscape
- Merge networks in Cytoscape and export as `master_network.graphml`