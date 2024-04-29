
# For four different networks, investigates robustness to node deletion. 
# For each network, nodes are deleted either randomly, or by selecting ones with the largest degree.
# The size of the largest conneted component as a function of the number nodes deleted is plotted. 


import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import numpy as np
#import pandas as pd
#import openpyxl

# iterations for the random deletions
iterations = 100


file_names = ['validated/validate-words19839.adjlist','validated/validate-lemma_words19839_1.adjlist','validated/validate-words74286.adjlist','validated/validate-lemma_words49690.adjlist']
file_titles = ['Words (n=19839)', 'Lemmas (n=19839)','All Words (n=74286)','All Lemmas (n=49690)']


# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(8, 8))

# Flatten the array of axes for easy iteration
axs = axs.flatten()

# Iterate over file names and axes
for file_name, ax, title in zip(file_names, axs,file_titles):


    G = nx.read_adjlist(file_name)


    n=G.number_of_nodes()
    e=G.number_of_edges()


    print("number of nodes",n)
    print("number of edges",e)



    # Replace G with its largest connected component
    connected_components = list(nx.connected_components(G))  # Get all connected components
    largest_component = max(connected_components, key=len)  # Find the largest one by length
    # Create a subgraph of G corresponding to the largest connected component
    G = G.subgraph(largest_component).copy()

    N = G.number_of_nodes()

    number_of_steps = 25
    M = N // number_of_steps


    num_nodes_removed = range(0, G.number_of_nodes(), M)
    #print('num_nodes_removed',num_nodes_removed)

    # Initialize storage for results
    all_random_attack_proportions = np.zeros((iterations, len(num_nodes_removed)))


    for iteration in range(iterations):
        C = G.copy()  # Reset C to the original graph at the beginning of each iteration
        random_attack_core_proportions = []
        for step, nodes_removed in enumerate(num_nodes_removed):

            # Measure the relative size of the network core
            if len(C) > 0:  # Ensure the graph still has nodes
                core = next(nx.connected_components(C), set())
                core_proportion = len(core) / N
            else:
                core_proportion = 0
            random_attack_core_proportions.append(core_proportion)
            
            # Remove nodes if there are enough nodes to remove
            if C.number_of_nodes() > M:
                nodes_to_remove = random.sample(list(C.nodes()), min(M, len(C)))
                C.remove_nodes_from(nodes_to_remove)
        
            
        
        # Store the results of this iteration
        all_random_attack_proportions[iteration] = random_attack_core_proportions

    # Calculate the average and standard error across iterations
    average_proportions = np.mean(all_random_attack_proportions, axis=0)
    #std_proportions = np.std(all_random_attack_proportions, axis=0, ddof=1)
    stderr_proportions = np.std(all_random_attack_proportions, axis=0, ddof=1) / np.sqrt(iterations)


    nodes_sorted_by_degree = sorted(G.nodes, key=G.degree, reverse=True)
    top_degree_nodes = nodes_sorted_by_degree[:M]


    num_nodes_removed = range(0, N, M)
    C = G.copy()
    targeted_attack_core_proportions = []
    for nodes_removed in num_nodes_removed:
        # Measure the relative size of the network core
        core = next(nx.connected_components(C))
        core_proportion = len(core) / N
        targeted_attack_core_proportions.append(core_proportion)
        
        # If there are more than M nodes, select top M nodes and remove them
        if C.number_of_nodes() > M:
            nodes_sorted_by_degree = sorted(C.nodes, key=C.degree, reverse=True)
            nodes_to_remove = nodes_sorted_by_degree[:M]
            C.remove_nodes_from(nodes_to_remove)


    ax.set_title(title)
    ax.set_xlabel("Number of nodes removed")
    ax.set_ylabel("Proportion of nodes in largest component")

  #  plt.title(title)
  #  plt.xlabel('Number of nodes removed')
  #  plt.ylabel('Proportion of nodes in largest component')
    ax.plot(num_nodes_removed, average_proportions, marker='o', label='Failures (avg)')
    ax.plot(num_nodes_removed, targeted_attack_core_proportions, marker='^', label='Attacks')


ax.legend()


# Adjust layout to prevent overlap
plt.tight_layout()

plt.show()

fig.savefig('node_removal.pdf')

