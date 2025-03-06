import network_utils
import click
import csv
import os

def get_all_neighbours_recursive(
	g,
	s,
	n,
	found_neighbors = None # This is crucial, if you initialize to [] it will be remembered and passed on to the next call, which causes a bug
):

	if found_neighbors is None:
		found_neighbors = []

	if n == 0:
		return(found_neighbors)
	else:
		#breakpoint()
		neighbours = list(g.neighbors(s))
		[found_neighbors.append(neighbour) for neighbour in neighbours if neighbour not in found_neighbors]
		for neighbour in neighbours:
			found_neighbors = get_all_neighbours_recursive(g, neighbour, n-1, found_neighbors)
	return(found_neighbors)


def query_neighbors(input_graphml, seeds, degree_of_neighborhood = 1):
	G_directed = network_utils.read_graphml(input_graphml)
	# Just for safety, should already be removed in cytoscape
	G_directed = network_utils.prune_nodes(G_directed)
	G_directed = network_utils.rename_nodes(G_directed, sel_substring = "KEGG_NODE_LABEL_LIST_FIRST", debug = True)
	G_undirected = G_directed.to_undirected()

	all_neighbors = {}
	for seed in seeds:
		if seed not in G_undirected.nodes:
			continue
		neighbors = get_all_neighbours_recursive(G_undirected, seed, degree_of_neighborhood)
		all_neighbors[seed] = neighbors
	return(all_neighbors)


def query_shortest_distance_single_network(input_graphml, ko_metabolite_csv):
	G_directed = network_utils.read_graphml(input_graphml)
	# Just for safety, should already be removed in cytoscape
	G_directed = network_utils.prune_nodes(G_directed)
	G_directed = network_utils.rename_nodes(G_directed, sel_substring = "KEGG_NODE_LABEL_LIST_FIRST", debug = True)

	kos, metabolites = network_utils.read_ko_metabolite_map(ko_metabolite_csv)

	queried_network_data = [network_utils.query_data(G_directed, ko, metabolite) for ko,metabolite in zip(kos, metabolites)]

	return(queried_network_data)

@click.group()
def get_ko_metabolite_shortest_distances():
	pass

@click.group()
def query_neighborhood():
	pass

@get_ko_metabolite_shortest_distances.command()
@click.option('--input_folder_graphml', help='Path to folder holding networks as graphml files.', default = 'networks_graphml', show_default = True)
@click.option('--ko_metabolite_csv', )
@click.option('--output_csv', help='Path to the output csv file.', default = 'ko_metabolite_shortest_distances.csv', show_default = True)
def query_shortest_distances(input_folder_graphml, ko_metabolite_csv, output_csv):
	"""
	Query the shortest distances between KOs and metabolites in the networks in the input folder.
	"""

	kos, metabolites = network_utils.read_ko_metabolite_map(ko_metabolite_csv)

	all_network_data = {}
	for network_file in os.listdir(input_folder_graphml):
		network_file_path = os.path.join(input_folder_graphml, network_file)
		network_res = query_shortest_distance_single_network(network_file_path, ko_metabolite_csv)
		all_network_data[network_file] = network_res
		click.echo(click.style(f"Successfully queried shortest distances between KOs and metabolites in {network_file_path}", fg='green'))
	
	all_found_paths = all_network_data.items()
	all_found_paths = [res for network_res in all_network_data.values() for res in network_res]
	all_found_paths = [res for res in all_found_paths if res[-1] != None]
	ko_metab_found = list(set([res[0:2] for res in all_found_paths]))

	for ko, metabolite in zip(kos, metabolites):
		if (ko, metabolite) not in ko_metab_found:
			click.echo(click.style(f"Warning: No network yielded any path between {ko} and {metabolite}. Consider checking your input mapping for spelling (or ignore this warning if you're sure about that)", fg='red'))
	

	with open(output_csv, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["network", "ko", "metabolite", "path_length", "directionality", "Path"])
		for network, network_res in all_network_data.items():
			for res in network_res:
				writer.writerow([network, *res])
	click.echo(f"Successfully wrote shortest distances between KOs and metabolites to {output_csv}")
	

@query_neighborhood.command()
@click.option('--input_folder_graphml', help='Path to folder holding networks as graphml files.', default = 'networks_graphml', show_default = True)
@click.option('--seed_file', help = 'path to 1-column txt file containing input seed names', default = 'seeds.txt', show_default = True)
@click.option('--degree_of_neighborhood', help='Degree of neighborhood to query', default = 1, show_default = True)
@click.option('--output_csv', help='Path to the output csv file.', default = 'neighborhoods.csv', show_default = True)
def query_neighborhoods(
	input_folder_graphml,
	seed_file,
	degree_of_neighborhood,
	output_csv,
):
	import pandas as pd

	def helper(e):
		if (isinstance(e, list) and len(e) > 0):
			return ",".join(e)
		else:
			return ""

	seeds = network_utils.read_seed_file(seed_file)

	all_neighbors = {}
	for network_file in os.listdir(input_folder_graphml):
		network_file_path = os.path.join(input_folder_graphml, network_file)
		neighbors_res = query_neighbors(network_file_path, seeds, degree_of_neighborhood=degree_of_neighborhood)
		all_neighbors[network_file] = neighbors_res
	
	df = pd.DataFrame(all_neighbors).transpose()
	# apply this logic to each column: replace NaNs with empty string, and join the list of neighbors with a comma
	df = df.applymap(helper)
	df.to_csv(output_csv)

	# TODO: Implement check similarly to above
	# TODO: Update README.md
	# TODO: Write Dimitris

cli = click.CommandCollection(sources=[get_ko_metabolite_shortest_distances, query_neighborhood])

if __name__ == "__main__":
	cli()