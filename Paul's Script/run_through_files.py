
# This runs through all the files and then outputs a table of basic statistics. 

import os
import pandas as pd
import networkx as nx
import openpyxl
import runpy
import time

import random

import networkx as nx
#import pandas as pd
import numpy as np
#from scipy.stats import lognorm, kstest
import powerlaw 
import matplotlib.pyplot as plt
import collections



start_time = time.time()


directory = 'validated'


# List to hold all the file data
data = []

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.adjlist'):  # or whatever file type you have
        filepath = os.path.join(directory, filename)
        print("file" ,filepath)

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
        print("number of nodes GC",largest_subgraph.number_of_nodes())
        print("number of edges GC",largest_subgraph.number_of_edges())


        # Average clustering coefficient for the graph
        avg_clustering_coefficient = nx.average_clustering(graph)       
        print("Average Clustering Coefficient:", avg_clustering_coefficient) 
        # average clustering component for the giant component
        avg_clustering_coefficient_GC = nx.average_clustering(largest_subgraph)
        print("Average Clustering Coefficient GC:", avg_clustering_coefficient_GC)
     
        # It's important to note that this calculation can be very intensive for large networks
        # compute average shortest path length    
        avg_shortest_path_length = nx.average_shortest_path_length(largest_subgraph)
        print("Average Shortest Path Length GC:", avg_shortest_path_length)


        # degree assortativity
        r = nx.degree_assortativity_coefficient(graph)
        print(f"Degree assortativity coefficient: {r}")
        r_GC = nx.degree_assortativity_coefficient(largest_subgraph)
        print(f"Degree assortativity coefficient of GC: {r_GC}")


        # Fraction of nodes in largest component
        fnlc = largest_subgraph.number_of_nodes()/graph.number_of_nodes()
        print(f"Fraction of nodes in largest component: {fnlc}")


        # will loop through this number of Erdos-Renyi graphs
        num_ER=10 
        
        # Lists to store the statistics for each of the ER graphs
        avg_clustering_coefficients_ER = []
        avg_clustering_coefficients_GC_ER = []
        avg_shortest_path_lengths_ER = []
        num_nodes_GC_ER = []
        num_edges_GC_ER = []

        # Run the simulation num_ER times
        for ERtrial in range(num_ER):
            
            print("ER trial number ",ERtrial)

            # Generate Erdős-Rényi graph with the same number of nodes and edges as connected component
            ER_graph = nx.gnm_random_graph(largest_subgraph.number_of_nodes(), largest_subgraph.number_of_edges())

            # get the largest connected component of ER graph
            connected_components_ER = sorted(nx.connected_components(ER_graph), key=len, reverse=True)
            # Extract the largest connected component
            largest_component_ER = connected_components_ER[0]
            # Create a subgraph of the graph containing only the nodes in the largest connected component
            largest_subgraph_ER = ER_graph.subgraph(largest_component_ER).copy()
          
            # average clustering coefficient for the ER graph
            avg_clustering_coefficient_ER = nx.average_clustering(ER_graph)
            print("Average Clustering Coefficient ER:", avg_clustering_coefficient_ER)

            # average clustering component for the giant component of ER graph
            avg_clustering_coefficient_GC_ER = nx.average_clustering(largest_subgraph_ER)
            print("Average Clustering Coefficient GC for ER:", avg_clustering_coefficient_GC_ER)

            print("number of nodes GC ER",largest_subgraph_ER.number_of_nodes())
            print("number of edges GC ER",largest_subgraph_ER.number_of_edges())

            avg_shortest_path_length_ER = nx.average_shortest_path_length(largest_subgraph_ER)
            print("Average Shortest Path Length GC ER:", avg_shortest_path_length_ER)

            # Store the results
            avg_clustering_coefficients_ER.append(avg_clustering_coefficient_ER)
            avg_clustering_coefficients_GC_ER.append(avg_clustering_coefficient_GC_ER)
            avg_shortest_path_lengths_ER.append(avg_shortest_path_length_ER)

        # Calculate the mean and standard deviation for each statistic
        mean_clustering_ER = np.mean(avg_clustering_coefficients_ER)
        std_clustering_ER = np.std(avg_clustering_coefficients_ER)

        mean_clustering_GC_ER = np.mean(avg_clustering_coefficients_GC_ER)
        std_clustering_GC_ER = np.std(avg_clustering_coefficients_GC_ER)

        mean_shortest_path_ER = np.mean(avg_shortest_path_lengths_ER)
        std_shortest_path_ER = np.std(avg_shortest_path_lengths_ER)

        mean_num_nodes_GC_ER = np.mean(num_nodes_GC_ER)
        std_num_nodes_GC_ER = np.std(num_nodes_GC_ER)

        mean_num_edges_GC_ER = np.mean(num_edges_GC_ER)
        std_num_edges_GC_ER = np.std(num_edges_GC_ER)

       
        #r_ER = nx.degree_assortativity_coefficient(ER_graph)
        #print(f"Degree assortativity coefficient for ER: {r_ER}")
        #r_GC_ER = nx.degree_assortativity_coefficient(largest_subgraph_ER)
        #print(f"Degree assortativity coefficient of GC for ER: {r_GC_ER}")


        #fnlc_ER = largest_subgraph_ER.number_of_nodes()/ER_graph.number_of_nodes()
        #print(f"Fraction of nodes in largest component: {fnlc_ER}")

        # Humphries-Gurney measure of small-world-ness
        S_HG = (avg_clustering_coefficient_GC/mean_clustering_GC_ER)/(avg_shortest_path_length/mean_shortest_path_ER)


        # Add a dictionary for the file with the parameters
        data.append({
            'Filename': filename,
            'Word or Lemma': filename.startswith('validate-lemma'),
            'Number of Nodes': graph.number_of_nodes(),
            'Number of Edges': graph.number_of_edges(),
            'Average clustering coefficient': avg_clustering_coefficient,
            'Average Clustering Coefficient GC': avg_clustering_coefficient_GC,            
            'Mean clustering coefficient for the ER graph': mean_clustering_ER,
            'Std Clustering Coefficient for ER': std_clustering_ER, 
            'Mean Clustering Coefficient GC for ER': mean_clustering_GC_ER,
            'Std Clustering Coefficient GC for ER': std_clustering_GC_ER, 
            'Average Shortest Path Length GC': avg_shortest_path_length,
            'Mean Shortest Path Length GC ER': mean_shortest_path_ER,
            'std Shortest Path Length GC ER': std_shortest_path_ER,
            'Number of nodes GC': largest_subgraph.number_of_nodes(),
            'Number of edges GC': largest_subgraph.number_of_edges(),
            'Humphries-Gurney measure of small-world-ness': S_HG,
            'Degree Assortativity': r,
            #'Degree Assortativity of ER': r_ER,
            'Degree assortativity coefficient of GC': r_GC,
            #'Degree assortativity coefficient of GC for ER': r_GC_ER,
            'Fraction of nodes in largest component': fnlc,
            #'Fraction of nodes in largest component ER': fnlc_ER,
            # Add other parameters here
        })

# Create a pandas DataFrame and print it, and sort it
df = pd.DataFrame(data)
df = df.sort_values(by=['Word or Lemma', 'Number of Nodes'])


# Print the DataFrame in a tabular format
print(df.to_string(index=False))

# Save to Excel file
df.to_excel(directory+'output.xlsx', index=False)  # Requires openpyxl or xlwt to be installed for .xlsx or .xls files respectively

end_time = time.time()
elapsed_time = end_time - start_time
print(f"The code took {elapsed_time} seconds to complete")

