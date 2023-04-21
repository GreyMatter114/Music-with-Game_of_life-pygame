import networkx as nx
from port import *
from skimage import measure

def render(adjacency_matrix):
    # Create a sample graph
    # Create a sample spatial graph
    # Convert the graph to an adjacency matrix
    # Convert the adjacency matrix to a NumPy arra
    # Create a sample boolean 2D matrix
    matrix = np.array(adjacency_matrix)

    # Find connected regions (islands) in the matrix
    label_matrix = measure.label(matrix)

    # Count the number of islands and their size
    num_islands = label_matrix.max()
    island_sizes = [np.sum(label_matrix == i) for i in range(1, num_islands+1)]

    # Print the results
    return island_sizes