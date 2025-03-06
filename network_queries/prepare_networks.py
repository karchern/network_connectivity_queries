import click
import py4cytoscape
import os

@click.group()
def load_sexport_sessions_to_graphml1():
    pass

def load_session_and_export_networks_to_graphml(session_file, output_folder):
    """
    Load a Cytoscape session using py4cytoscape and export all networks as GraphML files.

    :param session_file: Path to the Cytoscape session file.
    :param output_folder: Folder to export the GraphML files.
    """
    try:
        py4cytoscape.session.open_session(session_file)
        click.echo(f"Successfully loaded session from {session_file}")
        
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Get the list of all network SUIDs
        network_names = py4cytoscape.networks.get_network_list()
        network_suids = [py4cytoscape.networks.get_network_suid(n) for n in network_names]


        # Loop through each network and export it as a GraphML file
        for network_name, network_suid in zip(network_names, network_suids):
            network_name_no_fslash = network_name.replace("/", "___")
            output_file = os.path.join(output_folder, f"{network_name_no_fslash}.graphml") # Some network names contain slahes, which messes up file paths
            py4cytoscape.networks.export_network(output_file, 'graphml', network=network_suid, overwrite_file=True)
    
    except Exception as e:
        click.echo(f"Error: {e}")

@load_sexport_sessions_to_graphml1.command()
@click.option('--session_files', default='aux_scripts/cytoscape_session_files', show_default=True)
@click.option('--output_folder', default='networks_graphml', show_default=True)
def export_sessions_to_graphml(
    session_files, output_folder
):
    for session_file in os.listdir(session_files):
        session_file_path = os.path.join(session_files, session_file)
        load_session_and_export_networks_to_graphml(session_file_path, output_folder)
        click.echo(f"Successfully exported networks from {session_file_path} to {output_folder}")

#cli = click.CommandCollection(sources=[load_session1, load_all_networks1])
cli = click.CommandCollection(sources=[load_sexport_sessions_to_graphml1])

if __name__ == '__main__':
    cli()