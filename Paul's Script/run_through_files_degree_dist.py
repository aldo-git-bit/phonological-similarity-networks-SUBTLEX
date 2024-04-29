
#  Gives the best fit of lognormal and exponential distributions to degree distributions for each network. 
# It also gives the KS distance from the data to each distribution, as well as the power law and the truncated power law.


import os
import pandas as pd
import networkx as nx
import time
import numpy as np
from scipy.stats import lognorm, kstest
import powerlaw 


directory = 'validated'


# List to hold all the file data
data = []

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.adjlist'):  # or whatever file type you have
        filepath = os.path.join(directory, filename)

        print('filename: ',filename)

        graph = nx.read_adjlist(filepath)

        # find the largest connected component
        # Find all weakly connected components in the graph, sorted by size
        connected_components = sorted(nx.connected_components(graph), key=len, reverse=True)
        # Extract the largest connected component
        largest_component = connected_components[0]
        # Create a subgraph of the graph containing only the nodes in the largest connected component
        GC = graph.subgraph(largest_component).copy()


        print("number of nodes largest component",GC.number_of_nodes())
        print("number of edges largest component",GC.number_of_edges())


        # Calculate the degrees of the graph
        degrees = [degree for node, degree in GC.degree()]

        print("The first elements of the degrees list are:")
        print(degrees[:100])  # Prints the first 10 elements


        # Fit models to data over whole range. Select lognormal and exponential
        fit = powerlaw.Fit(degrees,discrete=True,xmin=1)
        fit_lognormal=fit.lognormal


        # Print the mu and sigma for the lognormal fit
        print(f'Lognormal mu: {fit_lognormal.mu}')
        print(f'lognormal sigma: {fit_lognormal.sigma}')

        fit_exponential=fit.exponential
    
        print(f'Exponential lambda: {fit_exponential.parameter1}')


        file_data = {
            'Filename': filename,
            'Word or Lemma': filename.startswith('validate-lemma'),
            'Number of Nodes': GC.number_of_nodes(),
            'Number of Edges': GC.number_of_edges(),
            'Mean degree': np.mean(degrees),
            'Std degree': np.std(degrees),
            'Max degree': np.max(degrees),
            'Lognormal mu' : fit_lognormal.mu,
            'Lognormal sigma' : fit_lognormal.sigma,
            'Exponential lambda' : fit_exponential.parameter1,
            'KS distance lognnormal': fit_lognormal.D,
            'KS distance exponential': fit_exponential.D,
            'KS distance power_law': fit.power_law.D,
            'KS distance truncated_power_law': fit.truncated_power_law.D
            # Add other parameters here if needed
        }

        data.append(file_data)


# Create a pandas DataFrame, and sort it
df = pd.DataFrame(data)
df = df.sort_values(by=['Word or Lemma', 'Number of Nodes'])


# Print the DataFrame in a tabular format
print(df.to_string(index=False))

# Save to Excel file
df.to_excel(directory+'output_degree_dist.xlsx', index=False)  # Requires openpyxl or xlwt to be installed for .xlsx or .xls files respectively

