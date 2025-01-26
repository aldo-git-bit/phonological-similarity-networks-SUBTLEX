# backbone extraction

import sys
import os
import pandas as pd
import networkx as nx
import openpyxl
import runpy
import time
import math

import random

import networkx as nx
#import pandas as pd
import numpy as np
from scipy.stats import t
import powerlaw 
import matplotlib.pyplot as plt
import collections

import community as louvain  # From python-louvain package

from networkx.algorithms.link_prediction import jaccard_coefficient


def welchs_t_test(mean1, std1, n1, mean2, std2, n2):
    # Calculate the t statistic
    t_statistic = (mean1 - mean2) / math.sqrt((std1**2 / n1) + (std2**2 / n2))
    
    # Calculate the degrees of freedom
    df = ((std1**2 / n1) + (std2**2 / n2))**2 / (
        ((std1**2 / n1)**2 / (n1 - 1)) + ((std2**2 / n2)**2 / (n2 - 1))
    )
    
    # Calculate the p-value (two-tailed)
    p_value = 2 * (1 - t.cdf(abs(t_statistic), df))
    
    print(f"T-statistic: {t_statistic}")
    print(f"P-value: {p_value}")
    print(f"Degrees of freedom: {df}")

    return t_statistic, p_value, df



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


def compute_graph_statistics(G):
    # Compute graph statistics for the entire graph
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    # Degree statistics
    degrees = [deg for _, deg in G.degree()]
    avg_degree = np.mean(degrees)
    std_degree = np.std(degrees)

    # Clustering coefficient statistics
    clustering_coeffs = list(nx.clustering(G).values())
    avg_clustering = np.mean(clustering_coeffs)
    std_clustering = np.std(clustering_coeffs)

    # Closeness centrality statistics
    closeness = list(nx.closeness_centrality(G).values())
    avg_closeness = np.mean(closeness)
    std_closeness = np.std(closeness)

    return {
        "Number of Nodes": num_nodes,
        "Average Degree": avg_degree,
        "Degree Standard Deviation": std_degree,
        "Clustering Coefficient": avg_clustering,
        "Clustering Standard Deviation": std_clustering,
        "Closeness Centrality": avg_closeness,
        "Closeness Standard Deviation": std_closeness
    }

def compare_subgraphs(original_graph, node_sets):
    stats_list = []

    # For each set of nodes, induce a subgraph and compute statistics
    for i, node_set in enumerate(node_sets, 1):
        subgraph = original_graph.subgraph(node_set).copy()  # Create induced subgraph
        subgraph_stats = compute_graph_statistics(subgraph)  # Compute stats for the subgraph
        stats_list.append(subgraph_stats)

    # Create a DataFrame to store the results
    df = pd.DataFrame(stats_list, index=[f"Subgraph {i+1}" for i in range(len(node_sets))])
    
    return df

def extract_giant_component_nodes(G):
    # Find the largest connected component (giant component)
    giant_component = max(nx.connected_components(G), key=len)
    return set(giant_component)

def write_nodes_to_file(filename, node_set):
    # Write the nodes to a file, one node per line
    with open(filename, 'w') as f:
        for node in node_set:
            f.write(f"{node}\n")

# Define a function to calculate statistics for filtered word data
def calculate_word_statistics(filtered_data):
    avg_log_frequency = filtered_data['log_frequency'].mean()
    std_log_frequency = filtered_data['log_frequency'].std()
    avg_length = filtered_data['New_World_Length'].mean()
    std_length = filtered_data['New_World_Length'].std()
    
    return {
        "Average Log Frequency": avg_log_frequency,
        "Log Frequency Standard Deviation": std_log_frequency,
        "Average Word Length": avg_length,
        "Word Length Standard Deviation": std_length
    }


start_time = time.time()

# Import the Excel file with word data
word_data = pd.read_excel('2024-10-07_words_giant_updated.xlsx')

# Calculate the log frequency using base 10 and add it as a new column
totwords_in_millions=49.719560
word_data['log_frequency'] = np.log10(word_data['frequency']/totwords_in_millions)

# Filter the data based on the "in_backbone" column and the node sets
all_nodes = word_data
backbone_nodes = word_data[word_data['giant'] == 'in']  
difference_nodes = word_data[word_data['giant'] == 'out']

# Compute statistics for each set of nodes
all_stats = calculate_word_statistics(all_nodes)
backbone_stats = calculate_word_statistics(backbone_nodes)
difference_stats = calculate_word_statistics(difference_nodes)


# Create a dictionary with the word statistics for each set
word_statistics = {
    "Average Log Frequency": [
        all_stats["Average Log Frequency"],
        backbone_stats["Average Log Frequency"],
        difference_stats["Average Log Frequency"]
    ],
    "Log Frequency Standard Deviation": [
        all_stats["Log Frequency Standard Deviation"],
        backbone_stats["Log Frequency Standard Deviation"],
        difference_stats["Log Frequency Standard Deviation"]
    ],
    "Average Word Length": [
        all_stats["Average Word Length"],
        backbone_stats["Average Word Length"],
        difference_stats["Average Word Length"]
    ],
    "Word Length Standard Deviation": [
        all_stats["Word Length Standard Deviation"],
        backbone_stats["Word Length Standard Deviation"],
        difference_stats["Word Length Standard Deviation"]
    ]
}

# Convert the dictionary into a DataFrame
word_statistics_df = pd.DataFrame(
    word_statistics,
    index=["Original Giant Component", "Backbone Giant Component", "Difference Nodes"]
)

# Display the DataFrame to ensure it's correct
print(word_statistics_df)



#sys.exit("Stopping the script here.")


#filename = 'validate-words8192.adjlist'
#filename = 'validate-words16384.adjlist'
filename = 'validate-words19839.adjlist'
#filename = 'validate-words74286.adjlist'

filepath = 'validated/' + filename
#filepath = 'validated/validate-words1024.adjlist'


original_network = nx.read_adjlist(filepath)
backbone = jaccard_top_edges_sparser(original_network,0.5)

# nodes in the giant component of original graph
original_giant_nodes = extract_giant_component_nodes(original_network)
backbone_nodes = extract_giant_component_nodes(backbone)
backbone_giant_nodes= original_giant_nodes & backbone_nodes
difference_nodes = original_giant_nodes - backbone_nodes


# Write the results to files
write_nodes_to_file('giant_component_original.txt', original_giant_nodes)
write_nodes_to_file('giant_component_backbone.txt', backbone_giant_nodes)
write_nodes_to_file('nodes_in_original_not_in_backbone.txt', difference_nodes)


# Compare the induced subgraphs from the node sets
comparison_df = compare_subgraphs(original_network, [original_giant_nodes, backbone_giant_nodes, difference_nodes])


# Create a list with the "Which Nodes" entries
which_nodes_entries = ["Original Giant Component", "Backbone Giant Component", "Difference Nodes"]

# Add the "Which Nodes" column to comparison_df
comparison_df.insert(0, "Which Nodes", which_nodes_entries)

# Display the comparison table
print(comparison_df)

# Ensure both DataFrames have the same index
comparison_df.index = ["Original Giant Component", "Backbone Giant Component", "Difference Nodes"]
word_statistics_df.index = ["Original Giant Component", "Backbone Giant Component", "Difference Nodes"]

# Join the DataFrames on the index
df = comparison_df.join(word_statistics_df)


# Save to Excel file
df.to_excel(filename+'compare_gc.xlsx', index=False)  # Requires openpyxl or xlwt to be installed for .xlsx or .xls files respectively


# do welch's t test for each column in the table, but only between last two rows
n1=df.loc['Backbone Giant Component','Number of Nodes']
n2=df.loc['Difference Nodes','Number of Nodes']
#print(df.iloc[2,1])
print(f"Degree")
print(f"{df.iloc[1,2], df.iloc[1,3], n1, df.iloc[2,2], df.iloc[2,3],n2}")
t_stat, p_val, degrees_of_freedom = welchs_t_test(df.iloc[1,2], df.iloc[1,3], n1, df.iloc[2,2], df.iloc[2,3], n2)
print(f"Clustering Coefficient")
print(f"{df.iloc[1,4], df.iloc[1,5], n1, df.iloc[2,4], df.iloc[2,5]}")
t_stat, p_val, degrees_of_freedom = welchs_t_test(df.iloc[1,4], df.iloc[1,5], n1, df.iloc[2,4], df.iloc[2,5], n2)
print(f"Closeness Centrality")
print(f"{df.iloc[1,6], df.iloc[1,7], n1, df.iloc[2,6], df.iloc[2,7]}")
t_stat, p_val, degrees_of_freedom = welchs_t_test(df.iloc[1,6], df.iloc[1,7], n1, df.iloc[2,6], df.iloc[2,7], n2)
print(f"Log Frequency")
print(f"{df.iloc[1,8], df.iloc[1,9], n1, df.iloc[2,8], df.iloc[2,9]}")
t_stat, p_val, degrees_of_freedom = welchs_t_test(df.iloc[1,8], df.iloc[1,9], n1, df.iloc[2,8], df.iloc[2,9], n2)
print(f"Word Length")
print(f"{df.iloc[1,10], df.iloc[1,11], n1, df.iloc[2,10], df.iloc[2,11]}")
t_stat, p_val, degrees_of_freedom = welchs_t_test(df.iloc[1,10], df.iloc[1,11], n1, df.iloc[2,10], df.iloc[2,11], n2)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"The code took {elapsed_time} seconds to complete")