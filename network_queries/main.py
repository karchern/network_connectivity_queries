import network_utils
import click
import csv

@click.command()
@click.option('--input_graphml', help='Path to the graphml file.', default = '/Users/karcher/network_connectivity_queries/master_network.graphml', show_default = True)
@click.option('--ko_metabolite_csv')
@click.option('--output_csv', help='Path to the output csv file.', default = '/Users/karcher/network_connectivity_queries/queried_network_results.csv', show_default = True)
def main(input_graphml, ko_metabolite_csv, output_csv):
	G_directed = network_utils.read_graphml(input_graphml)
	# Just for safety, should already be removed in cytoscape
	G_directed = network_utils.prune_map_nodes(G_directed)
	G_directed = network_utils.rename_nodes(G_directed, sel_substring = "KEGG_NODE_LABEL_LIST_FIRST", debug = False)

	kos, metabolites = network_utils.read_ko_metabolite_map(ko_metabolite_csv)

	queried_network_data = [network_utils.query_data(G_directed, ko, metabolite) for ko,metabolite in zip(kos, metabolites)]

	# Open a file in write mode
	with open(output_csv, mode='w', newline='') as file:
		writer = csv.writer(file)
		
		# Write the data rows
		for row in queried_network_data:
			# if isinstance(row, NoneType):
			# 	breakpoint()
			print(row)
			writer.writerow(row)
	

if __name__ == "__main__":
	main()