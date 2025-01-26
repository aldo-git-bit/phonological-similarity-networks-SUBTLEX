
setwd("/Users/paultupper/Library/CloudStorage/Dropbox/python projects/python_network_testing/for sarbjot good version of code/validated")

# Create a graph using the igraph package
library(igraph)


# Install the backbone package from CRAN
install.packages("backbone")

# Load the backbone package
library(backbone)

# Step 1: Read the file
#file_path <- "validate-words19839.adjlist"
file_path <- "validate-words16384.adjlist"
lines <- readLines(file_path)

# Step 2: Initialize lists for nodes and edges
nodes <- c()  # To store unique nodes
edges <- list()  # To store the edges

# Step 3: Process the file line by line
for (line in lines) {
  # Skip comments
  if (grepl("^#", line)) next
  
  # Split the line into words (first word is the node, others are adjacent nodes)
  words <- unlist(strsplit(line, " "))
  
  # Add the first word as a node (even if it has no edges)
  if (length(words) > 0) {
    node <- words[1]
    
    # Add node to the list of nodes
    nodes <- unique(c(nodes, node))  # Ensure nodes are unique
    
    # If there are adjacent nodes, create edges
    if (length(words) > 1) {
      adjacent_nodes <- words[-1]
      
      # Create edges between the node and its adjacent nodes
      new_edges <- cbind(rep(node, length(adjacent_nodes)), adjacent_nodes)
      edges <- rbind(edges, new_edges)
    }
  }
}

# Step 4: Create a data frame of nodes and edges
# Ensure edges is a data frame if edges were created
if (length(edges) > 0) {
  edges_df <- as.data.frame(edges, stringsAsFactors = FALSE)
  colnames(edges_df) <- c("from", "to")
}


# Create a graph using the nodes and edges
# Ensure nodes with no edges are included
g <- graph_from_data_frame(d = if (exists("edges_df")) edges_df else NULL, vertices = nodes, directed = FALSE)

# View the graph's details (number of nodes and edges)
print(paste("Number of nodes:", vcount(g)))
print(paste("Number of edges:", ecount(g)))



bb <- sparsify.with.lspar(g, s = 0.)

# View the graph's details (number of nodes and edges)
print(paste("Number of nodes:", vcount(g)))
print(paste("Number of edges:", ecount(g)))
# View the graph's details (number of nodes and edges)
print(paste("Number of nodes backbone:", vcount(bb)))
print(paste("Number of edges backbone", ecount(bb)))


