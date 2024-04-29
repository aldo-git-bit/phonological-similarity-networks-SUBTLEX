
# This runs through all the files and then outputs a table of basic statistics. 

import os
import pandas as pd
import networkx as nx
import openpyxl
import runpy
import time

directory = 'validated'


# List to hold all the file data
data = []

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.adjlist'):  # or whatever file type you have
        filepath = os.path.join(directory, filename)

        start_time = time.time()


        graph = nx.read_adjlist(filepath)

        print("number of nodes",graph.number_of_nodes())
        print("number of edges",graph.number_of_edges())


        # find the largest connected component
        # Find all weakly connected components in the graph, sorted by size
        connected_components = sorted(nx.connected_components(graph), key=len, reverse=True)
        # Extract the largest connected component
        largest_component = connected_components[0]
        # Create a subgraph of the graph containing only the nodes in the largest connected component
        largest_subgraph = graph.subgraph(largest_component).copy()

        # Generate Erdős-Rényi graph with the same number of nodes and edges as connected component
        ER_graph = nx.gnm_random_graph(largest_subgraph.number_of_nodes(), largest_subgraph.number_of_edges())

        # do the same for erdos-renyi graph
        connected_components_ER = sorted(nx.connected_components(ER_graph), key=len, reverse=True)
        # Extract the largest connected component
        largest_component_ER = connected_components_ER[0]
        # Create a subgraph of the graph containing only the nodes in the largest connected component
        largest_subgraph_ER = ER_graph.subgraph(largest_component_ER).copy()



        # Average clustering coefficient for the graph
        avg_clustering_coefficient = nx.average_clustering(graph)       
        print("Average Clustering Coefficient:", avg_clustering_coefficient)       
        # average clustering coefficient for the ER graph
        avg_clustering_coefficient_ER = nx.average_clustering(ER_graph)
        print("Average Clustering Coefficient ER:", avg_clustering_coefficient_ER)


        # average clustering component for the giant component
        avg_clustering_coefficient_GC = nx.average_clustering(largest_subgraph)
        print("Average Clustering Coefficient GC:", avg_clustering_coefficient_GC)
        # average clustering component for the giant component of ER graph
        avg_clustering_coefficient_GC_ER = nx.average_clustering(largest_subgraph_ER)
        print("Average Clustering Coefficient GC for ER:", avg_clustering_coefficient_GC_ER)


    


        print("number of nodes GC",largest_subgraph.number_of_nodes())
        print("number of edges GC",largest_subgraph.number_of_edges())

        print("number of nodes GC ER",largest_subgraph_ER.number_of_nodes())
        print("number of edges GC ER",largest_subgraph_ER.number_of_edges())




        # It's important to note that this calculation can be very intensive for large networks
        avg_shortest_path_length = nx.average_shortest_path_length(largest_subgraph)
        print("Average Shortest Path Length GC:", avg_shortest_path_length)
        avg_shortest_path_length_ER = nx.average_shortest_path_length(largest_subgraph_ER)
        print("Average Shortest Path Length GC ER:", avg_shortest_path_length_ER)


        # degree assortativity
        r = nx.degree_assortativity_coefficient(graph)
        print(f"Degree assortativity coefficient: {r}")
        r_GC = nx.degree_assortativity_coefficient(largest_subgraph)
        print(f"Degree assortativity coefficient of GC: {r_GC}")
        r_ER = nx.degree_assortativity_coefficient(ER_graph)
        print(f"Degree assortativity coefficient for ER: {r_ER}")
        r_GC_ER = nx.degree_assortativity_coefficient(largest_subgraph_ER)
        print(f"Degree assortativity coefficient of GC for ER: {r_GC_ER}")


        # Fraction of nodes in largest component
        fnlc = largest_subgraph.number_of_nodes()/graph.number_of_nodes()
        print(f"Fraction of nodes in largest component: {fnlc}")
        fnlc_ER = largest_subgraph_ER.number_of_nodes()/ER_graph.number_of_nodes()
        print(f"Fraction of nodes in largest component: {fnlc_ER}")


        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"The code took {elapsed_time} seconds to complete")




        # Add a dictionary for the file with the parameters
        data.append({
            'Filename': filename,
            'Number of Nodes': graph.number_of_nodes(),
            'Number of Edges': graph.number_of_edges(),
            'Average clustering coefficient': avg_clustering_coefficient,
            'Average Clustering Coefficient GC': avg_clustering_coefficient_GC,            
            'average clustering coefficient for the ER graph': avg_clustering_coefficient_ER,
            'Average Clustering Coefficient GC for ER': avg_clustering_coefficient_GC_ER,
            'Average Shortest Path Length GC': avg_shortest_path_length,
            'Average Shortest Path Length GC ER': avg_shortest_path_length_ER,
            'Number of nodes GC': largest_subgraph.number_of_nodes(),
            'Number of edges GC': largest_subgraph.number_of_edges(),
            'Degree Assortativity': r,
            'Degree Assortativity of ER': r_ER,
            'Degree assortativity coefficient of GC': r_GC,
            'Degree assortativity coefficient of GC for ER': r_GC_ER,
            'Fraction of nodes in largest component': fnlc,
            'Fraction of nodes in largest component ER': fnlc_ER,
            # Add other parameters here
        })

# Create a pandas DataFrame and print it
df = pd.DataFrame(data)

# Print the DataFrame in a tabular format
print(df.to_string(index=False))

# Save to Excel file
df.to_excel(directory+'output.xlsx', index=False)  # Requires openpyxl or xlwt to be installed for .xlsx or .xls files respectively

