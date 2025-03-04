import networkx as nx

def read_ko_metabolite_map(
	ko_metabolite_map,
	delim = ','
):
	kos = []
	metabolites = []
	with open(ko_metabolite_map, 'r') as f:
		for line in f:
			ko, metabolite = line.strip().split(delim)
			kos.append(ko)
			metabolites.append(metabolite)
	return kos, metabolites

def split_edges(network_object):
	# Create a copy of the network to avoid modifying the original while iterating
	network_copy = network_object.copy()
    
	# Loop over each edge in the network
	for source, target, edge_data in network_object.edges(data=True):
		# Create a new node with the same attributes as the current edge
		new_node = f"{source}_{target}_split"

		# edge_data['KEGG_NODE_LABEL_LIST_FIRST'] = edge_data['KEGG_REACTION_GENE']
		# edge_data['KEGG_NODE_LABEL_LIST_FIRST'] = edge_data['KEGG_NODE_LABEL_LIST_FIRST'].replace('bvu:', "")
				
		for identifier in edge_data['KEGG_REACTION_GENE'].split(" "):
			identifier = identifier.replace('bvu:', "")
			edge_data['KEGG_NODE_LABEL_LIST_FIRST'] = identifier
			network_copy.add_node(new_node, **edge_data)
			
			# Add two new edges connecting the new node to the source and target nodes
			# network_copy.add_edge(source, new_node, **edge_data)
			# network_copy.add_edge(new_node, target, **edge_data)
			network_copy.add_edge(source, new_node)
			network_copy.add_edge(new_node, target)		

        # Remove the original edge
		network_copy.remove_edge(source, target)
    
	return network_copy

def render_path_readable(
	ko, 
	metabolite,
	p, 
	ko_upstream) :
	if p is None:
		print("PATH length NA;")
		return (None, None, None, None, None)
	path_readable = " -> ".join(p)
	print(f"{ko}, {metabolite}, PATH length {int(len(p)/2)} and {'ko is upstream' if ko_upstream else 'ko is downstream'}: {path_readable}")
	return (
		ko, metabolite, int(len(p)/2),'ko is upstream' if ko_upstream else 'ko is downstream', path_readable
	)

def rename_nodes(
	graph_object,
	sel_substring = None,
	debug = False
	):
	#node_mapping = {node: graph_object.nodes[node]['KEGG_NODE_LABEL_LIST_FIRST'].replace('...', "") for node in graph_object.nodes()}
	node_mapping = []
	for node in graph_object.nodes():
		# try:
		# 	KEGG_NODE_LABEL_LIST_FIRST = graph_object.nodes[node][sel_substring]
		# except:
		# 	print(f"Error: {sel_substring} not found for in node object {node}. Set Debug = True and execute this to understand what's going on: graph_object.nodes[node]. Entry in field KEGG_NODE_LABEL: {graph_object.nodes[node]['KEGG_NODE_LABEL']}")
		# 	if debug:
		# 		breakpoint()
		if sel_substring in graph_object.nodes[node]:
			KEGG_NODE_LABEL_LIST_FIRST = graph_object.nodes[node][sel_substring]
		elif "KEGG_NODE_LABEL" in graph_object.nodes[node]:
			KEGG_NODE_LABEL_LIST_FIRST = graph_object.nodes[node]["KEGG_NODE_LABEL"]
		else:
			print(f"""
			Error: {sel_substring} and KEGG_NODE_LABEL not found for in node object {node}. Set Debug = True and execute this to understand what's going on: graph_object.nodes[node].
			""")
			if debug:
				breakpoint()
			
		KEGG_NODE_LABEL_LIST_FIRST = KEGG_NODE_LABEL_LIST_FIRST.replace('...', "")
		node_mapping.append((node, KEGG_NODE_LABEL_LIST_FIRST))
	node_mapping = dict(node_mapping)
	graph_object = nx.relabel_nodes(graph_object, node_mapping)
	return graph_object


def read_graphml(in_graphml_path):
	return nx.read_graphml(in_graphml_path)
	

def get_shortest_path_between_KO_and_metabolite(
	graph_object,
	ko_of_interest,
	metabolite_of_interest,
	debug = False
):

	if debug:
		print(f"Finding shortest path between {ko_of_interest} and {metabolite_of_interest}")
	# Note: Add this point graph has a node for both KO as well as metabolite. 
	# This is actually very convenient, I think, because nx.shortest_path will be applicable as is
	try:
		shortest_path = nx.shortest_path(graph_object, ko_of_interest, metabolite_of_interest)
	except nx.NetworkXNoPath:
		if debug:
			print(f"No path found between {ko_of_interest} and {metabolite_of_interest}")
		shortest_path = []
	except nx.NodeNotFound:
		if debug:
			print(f"Error: Either {ko_of_interest} or {metabolite_of_interest} not found in graph")
		shortest_path = []
	return shortest_path

def prune_map_nodes(graph_object):
	# Remove map nodes (blue big nodes in cytoscape)
	nodes_to_remove = []
	for node in graph_object.nodes():
		if graph_object.nodes[node]['KEGG_NODE_TYPE'] == 'map':
			nodes_to_remove.append(node)
	graph_object.remove_nodes_from(nodes_to_remove)
	return graph_object

def ensure_shortest_path_makes_sense(path_list):
	if path_list is None:
		return None
	if len(path_list) == 0:
		return(path_list)
	# ensure path length is even
	if len(path_list) % 2 != 0:
		exit("Error: Path length is not even")
	if not "BVU" in path_list[0]:
		exit("Error: Path does not start with a KO node")
	if "BVU" in path_list[-1]:
		exit("Error: Path does not end with a metabolite node")
	for i, node in enumerate(path_list):
		if i == 0:
			continue
		if "BVU" in node:
			if "BVU" in path_list[i-1]:
				exit("Error: Two consecutive KO nodes in path")
		else:
			if "BVU" not in path_list[i-1]:
				exit("Error: Two consecutive metabolite nodes in path")
	return(path_list)


def query_data(
	G_directed,
	ko,
	metabolite
):
	# This could be slow in the long run, but is saver
	G_undirected = G_directed.to_undirected()
	# if len(G_directed.nodes) != len(G_undirected.nodes):
	# 	print("Error: Number of nodes in directed and undirected graph are not the same. Please ensure that G_undirected comes from G_directed.to_undirected()")
	# 	return None
	
	# if len(G_directed.edges) != len(G_undirected.edges):
	# 	print("Error: Number of edges in directed and undirected graph are not the same. Please ensure that G_undirected comes from G_directed.to_undirected()")
	# 	return None	
	shortest_path_directed = get_shortest_path_between_KO_and_metabolite(G_directed, ko, metabolite, debug = False)
	shortest_path_undirected = get_shortest_path_between_KO_and_metabolite(G_undirected, ko, metabolite, debug = False)
	shortest_path_directed = ensure_shortest_path_makes_sense(shortest_path_directed)
	shortest_path_undirected = ensure_shortest_path_makes_sense(shortest_path_undirected)
	if len(shortest_path_directed) == 0:
		if len(shortest_path_undirected) == 0:
			print(f"Path length NA: No path found linking {ko} and {metabolite}")
			return (ko, metabolite, None, None, None)
	if len(shortest_path_directed) != 0:
		ko_upstream = True
	else:
		ko_upstream = False
	return(render_path_readable(
		ko,
		metabolite,
		shortest_path_undirected, 
		ko_upstream))
