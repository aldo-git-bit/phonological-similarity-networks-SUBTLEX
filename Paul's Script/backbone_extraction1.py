# backbone extraction
# creating the analogue of table 2 in Vitevitch and Sale

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

import community as louvain  # From python-louvain package

from networkx.algorithms.link_prediction import jaccard_coefficient

def jaccard_top_edges_sparser(G, s):
    # Step 1: Compute Jaccard index only for existing edges
    existing_edges = list(G.edges())
    jaccard_similarities = list(jaccard_coefficient(G, existing_edges))

    # Step 2: Organize Jaccard similarities by node
    node_jaccard_dict = {node: [] for node in G.nodes()}

    for u, v, p in jaccard_similarities:
        # Store the Jaccard coefficient for both nodes (u and v)
        node_jaccard_dict[u].append((v, p))
        node_jaccard_dict[v].append((u, p))
    
    # Step 3: For each node, compute d^s and keep only the top d^s edges
    edges_to_keep = set()
    for node, neighbors in node_jaccard_dict.items():
        degree = G.degree[node]
        num_to_keep = max(1, int(degree**s))  # Ensure at least one edge is kept

        # Sort the neighbors by Jaccard similarity score in descending order
        neighbors.sort(key=lambda x: x[1], reverse=True)

        # Keep only the top d^s neighbors
        for neighbor, similarity in neighbors[:num_to_keep]:
            # Ensure that edges are added only once (to avoid duplication)
            edges_to_keep.add((min(node, neighbor), max(node, neighbor)))

    # Step 4: Create a new sparser graph with the retained edges
    sparser_graph = nx.Graph()
    sparser_graph.add_nodes_from(G.nodes())  # Add all nodes from the original graph
    sparser_graph.add_edges_from(edges_to_keep)  # Add only the retained edges
    
    return sparser_graph


def compute_graph_statistics(graph):

    #print("number of nodes",graph.number_of_nodes())
    #print("number of edges",graph.number_of_edges())

    # find the largest connected component
    # Find all weakly connected components in the graph, sorted by size
    connected_components = sorted(nx.connected_components(graph), key=len, reverse=True)
    # Extract the largest connected component
    largest_component = connected_components[0]
    # Create a subgraph of the graph containing only the nodes in the largest connected component
    largest_subgraph = graph.subgraph(largest_component).copy()
    #print("number of nodes GC",largest_subgraph.number_of_nodes())
    #print("number of edges GC",largest_subgraph.number_of_edges())


    avg_degree = sum(dict(graph.degree()).values()) / len(graph)
    #print(f"Average degree: {avg_degree}")
    avg_degree_GC = sum(dict(largest_subgraph.degree()).values()) / len(largest_subgraph)
    #print(f"Average degree GC: {avg_degree_GC}")

    # Diameter GC
    diameter = nx.diameter(largest_subgraph)
    #print("Diameter:", diameter)

    # It's important to note that this calculation can be very intensive for large networks
    # compute average shortest path length    
    avg_shortest_path_length = nx.average_shortest_path_length(largest_subgraph)
    #print("Average Shortest Path Length GC:", avg_shortest_path_length)

    # Get the number of connected components
    num_components = nx.number_connected_components(graph)

    # Find all isolates (nodes with no edges)
    isolates = list(nx.isolates(graph))

    # Subtract the number of isolates from the total number of connected components
    num_components_minus_isolates = num_components - len(isolates)

    #print(f"Number of connected components minus isolates: {num_components_minus_isolates}")

    components = list(nx.connected_components(graph))
    
    # Sort components by size (largest first)
    components.sort(key=len, reverse=True)
    
    # Remove isolates (components of size 1)
    non_isolate_components = [c for c in components if len(c) > 1]
    
    # Exclude the giant component (the largest one)
    if len(non_isolate_components) > 1:
        largest_non_giant = len(non_isolate_components[1])  # Second largest after excluding the giant
    else:
        largest_non_giant = 0  # No other components except the giant

    # Size of the smallest connected component (excluding isolates and the giant component)
    smallest_component = min(len(c) for c in non_isolate_components[1:]) if len(non_isolate_components) > 1 else 0
    

    # Average clustering coefficient for the graph
    avg_clustering_coefficient = nx.average_clustering(graph)       
    #print("Average Clustering Coefficient:", avg_clustering_coefficient) 

    # Perform Louvain community detection
    partition = louvain.best_partition(graph)


    return {
        "Num Nodes": graph.number_of_nodes(),
        "Num Edges": graph.number_of_edges(),
        "Num Nodes GC": largest_subgraph.number_of_nodes(),
        "Num Edges GC": largest_subgraph.number_of_edges(),
        "Ave Degree": avg_degree,
        "Ave Degree GC": avg_degree_GC,
        "Diameter": diameter,
        "ASPL": avg_shortest_path_length,
        "Num Con Comp (no GC)": num_components_minus_isolates-1,
        "Max Component Size": largest_non_giant,
        "Min Component Size": smallest_component,
        "Num Isolates": len(isolates),
        "Avg Clust Coef": avg_clustering_coefficient,
        "Num Communities": len(set(partition.values())),
        "Modularity (Q Value)": louvain.modularity(partition, graph)
    }
    

start_time = time.time()



#filename = 'validate-words8192.adjlist'
#filename = 'validate-words16384.adjlist'
filename = 'validate-words19839.adjlist'
#filename = 'validate-words74286.adjlist'

filepath = 'validated/' + filename
#filepath = 'validated/validate-words1024.adjlist'


original_network = nx.read_adjlist(filepath)
backbone = jaccard_top_edges_sparser(original_network,0.5)

# Compute statistics for both graphs
graph_stats = []
graph_stats.append(compute_graph_statistics(original_network))
graph_stats.append(compute_graph_statistics(backbone))

# Create a DataFrame to store the results
#df = pd.DataFrame(graph_stats, index=["Original Network"])
df = pd.DataFrame(graph_stats, index=["Original", "Backbone"])


# Display the DataFrame
print(df)


# Save to Excel file
df.to_excel(filename+'backbone.xlsx', index=False)  # Requires openpyxl or xlwt to be installed for .xlsx or .xls files respectively


end_time = time.time()
elapsed_time = end_time - start_time
print(f"The code took {elapsed_time} seconds to complete")