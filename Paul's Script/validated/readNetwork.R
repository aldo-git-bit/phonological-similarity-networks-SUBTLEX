
# Install the backbone package from CRAN
install.packages("backbone")

# Load the backbone package
library(backbone)

# Install the igraph package if not already installed
install.packages("igraph")

# Load igraph
library(igraph)

# Step 1: Read the file
file_path <- "validate-words19839.adjlist"
lines <- readLines(file_path)

# Step 2: Process the file line by line
edges <- list()  # To store the edges

for (line in lines) {
  # Skip comments and empty lines
  if (grepl("^#", line) || line == "") {
    print("This line is empty or a comment.")
    next
  }
    
  # Split the line into words (first word is the node, others are adjacent nodes)
  words <- unlist(strsplit(line, " "))
  if (length(words) > 1) {
    node <- words[1]
    adjacent_nodes <- words[-1]
    
    # Create edges between the node and its adjacent nodes
    new_edges <- cbind(rep(node, length(adjacent_nodes)), adjacent_nodes)
    edges <- rbind(edges, new_edges)
  }
}

# Step 3: Convert the list of edges to a data frame
edges_df <- as.data.frame(edges, stringsAsFactors = FALSE)
colnames(edges_df) <- c("from", "to")

# View the edge list
print(head(edges_df))

# Step 4: Create a graph using the igraph package
library(igraph)
g <- graph_from_data_frame(edges_df, directed = FALSE)

# Step 5: Plot the graph
#plot(g, vertex.label = V(g)$name)

# Assuming adj_matrix is your adjacency matrix
# Modify the sparsify function call to include s = 0
#bb <- sparsify(
#  U = adj_matrix,          # Your adjacency matrix
#  escore = "jaccard",      # Use Jaccard similarity score
#  normalize = "rank",      # Normalize by rank
#  filter = "degree",       # Filter by degree
#  umst = FALSE,            # Disable uniform minimum spanning tree
#  s = 0                    # Set sparsification parameter to 0
#)

# View the backbone
#print(bb)

bb <- sparsify.with.lspar(g, escore = "jaccard", normalize = "rank", s = 0., filter = "degree",  umst = FALSE)
bb <- sparsify.with.lspar(g, s = 0.)


