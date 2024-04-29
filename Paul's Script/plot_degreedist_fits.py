
# plots degree distributions with model fits for some of the networks

import networkx as nx
#import pandas as pd
import numpy as np
#from scipy.stats import lognorm, kstest
import powerlaw 
import matplotlib.pyplot as plt
import collections

#filename = 'Validated/lemma/validate-lemma_words1024_3.adjlist'
#filename = 'Validated/wordforms/validate-words1024.adjlist'
file_names = ['validated/validate-words19839.adjlist','validated/validate-lemma_words19839_1.adjlist','validated/validate-words74286.adjlist','validated/validate-lemma_words49690.adjlist']
file_titles = ['Words (n=19839)', 'Lemmas (n=19839)','All Words (n=74286)','All Lemmas (n=49690)']



# Create a 2x2 grid of subplots
fig, axs = plt.subplots(2, 2, figsize=(8, 8))

# Flatten the array of axes for easy iteration
axs = axs.flatten()

# Iterate over file names and axes
for file_name, ax, title in zip(file_names, axs,file_titles):

    graph = nx.read_adjlist(file_name)

    # find the largest connected component
    # Find all weakly connected components in the graph, sorted by size
    connected_components = sorted(nx.connected_components(graph), key=len, reverse=True)
    # Extract the largest connected component
    largest_component = connected_components[0]
    # Create a subgraph of the graph containing only the nodes in the largest connected component
    GC = graph.subgraph(largest_component).copy()
    
    # Calculate the degrees of the graph
    degrees = [degree for node, degree in GC.degree()]


    powerlaw.plot_pdf(degrees,color='b',ax=ax,label='Data',linewidth=2 )
    fit = powerlaw.Fit(degrees,discrete=True,xmin=1)
    fit.power_law.plot_pdf(color='r', linestyle='--', label='Power law fit', ax=ax)
    fit.exponential.plot_pdf(color='g', linestyle='--', label='Exponential fit', ax=ax)
    fit.truncated_power_law.plot_pdf(color='purple', linestyle='--', label='Truncated Power law fit', ax=ax)
    fit.lognormal.plot_pdf(color='magenta', linestyle='--', label='Lognormal fit', ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Degree")
    ax.set_ylabel("Frequency")
    #ax.legend()




    #ax.set_ylim(1e-4, 2e-1)

ax.legend()


# Adjust layout to prevent overlap
plt.tight_layout()

plt.show()

fig.savefig('degree_dists.pdf')
