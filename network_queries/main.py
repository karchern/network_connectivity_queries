import network_utils
import click
import csv
import os


def query_shortest_distance_single_network(input_graphml, ko_metabolite_csv):
	G_directed = network_utils.read_graphml(input_graphml)
	# Just for safety, should already be removed in cytoscape
	G_directed = network_utils.prune_map_nodes(G_directed)
	G_directed = network_utils.rename_nodes(G_directed, sel_substring = "KEGG_NODE_LABEL_LIST_FIRST", debug = False)

	kos, metabolites = network_utils.read_ko_metabolite_map(ko_metabolite_csv)

	queried_network_data = [network_utils.query_data(G_directed, ko, metabolite) for ko,metabolite in zip(kos, metabolites)]

	return(queried_network_data)

@click.group()
def get_ko_metabolite_shortest_distances():
	pass

@get_ko_metabolite_shortest_distances.command()
@click.option('--input_folder_graphml', help='Path to folder holding networks as graphml files.', default = 'networks_graphml', show_default = True)
@click.option('--ko_metabolite_csv', )
@click.option('--output_csv', help='Path to the output csv file.', default = 'ko_metabolite_shortest_distances', show_default = True)
def query_shortest_distances(input_folder_graphml, ko_metabolite_csv, output_csv):
	"""
	Query the shortest distances between KOs and metabolites in the networks in the input folder.
	"""
	all_network_data = {}
	for network_file in os.listdir(input_folder_graphml):
		network_file_path = os.path.join(input_folder_graphml, network_file)
		network_res = query_shortest_distance_single_network(network_file_path, ko_metabolite_csv)
		all_network_data[network_file] = network_res
		click.echo(f"Successfully queried shortest distances between KOs and metabolites in {network_file_path}")
	breakpoint()

cli = click.CommandCollection(sources=[get_ko_metabolite_shortest_distances])

if __name__ == "__main__":
	cli()