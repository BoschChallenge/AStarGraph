import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

def euclidean_distance(u, v, node_positions):
    x1, y1 = node_positions[u]
    x2, y2 = node_positions[v]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def manhattan_distance(u, v, node_positions):
    x1, y1 = node_positions[u]
    x2, y2 = node_positions[v]
    return abs(x2 - x1) + abs(y2 - y1)

def astar_path(graph, start, goal, heuristic=None):
    if heuristic is None:
        def heuristic(u, v):
            return 0  # No heuristic, uniform cost search

    path = nx.astar_path(graph, start, goal, heuristic=heuristic)
    return path

# Read the GraphML file
G = nx.read_graphml('C:\\Users\\Lejk\\Documents\\BFMC\\TestAStar\\Competition_track_graph.graphml')

# Extract node positions from the 'data' attributes
node_positions = {node: (float(data.get('x', 0)), -float(data.get('y', 0))) for node, data in G.nodes(data=True)}

# Filter out nodes without 'x' and 'y' attributes
node_positions = {node: pos for node, pos in node_positions.items() if all(pos)}

# Convert node IDs to strings for consistency
node_positions = {str(node): pos for node, pos in node_positions.items()}

# If the node positions look correct, proceed to drawing edges
# Extract edge attributes (dotted or continuous line)
edge_attributes = nx.get_edge_attributes(G, 'dotted')
dotted_edges = [edge for edge, dotted in edge_attributes.items() if dotted]
solid_edges = [edge for edge in G.edges() if edge not in dotted_edges]

# Prompt user to input start and end nodes
start_node = input("Enter the start node: ")
goal_node = input("Enter the goal node: ")

# Find the A* path
path = astar_path(G, start_node, goal_node, heuristic=lambda u, v: manhattan_distance(u, v, node_positions))

# Convert node names in the path to integers
path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

# Draw the graph with the A* path
fig, ax = plt.subplots(figsize=(16, 9))
nx.draw_networkx_edges(G, pos=node_positions, edgelist=dotted_edges, edge_color='orange', style='dashed', width=1, alpha=0.7)
nx.draw_networkx_edges(G, pos=node_positions, edgelist=solid_edges, edge_color='blue', width=1.5, alpha=0.7)
nx.draw_networkx_nodes(G, pos=node_positions, node_size=20, node_color='blue')
nx.draw_networkx_nodes(G, pos=node_positions, nodelist=[start_node], node_size=50, node_color='green')
nx.draw_networkx_nodes(G, pos=node_positions, nodelist=[goal_node], node_size=50, node_color='red')
plt.axis('off')

def update(frame):
    plt.clf()
    # Color all edges blue by default, and dotted edges orange
    edge_colors = {edge: 'orange' if edge in dotted_edges else 'blue' for edge in G.edges()}
    # Color the edges in the path green if passed, or red if current
    for i in range(len(path_edges)):
        if i < frame:
            edge_colors[path_edges[i]] = 'green'  
            # Edge has been covered
        elif i == frame:
            edge_colors[path_edges[i]] = 'red'
            # Current edge
        # Draw solid edges first
    nx.draw_networkx_edges(G, pos=node_positions, edgelist=[e for e in solid_edges if e in edge_colors],
                               edge_color=[edge_colors[e] for e in solid_edges if e in edge_colors], width=1.5, alpha=0.7)
    # Draw dotted edges
    nx.draw_networkx_edges(G, pos=node_positions, edgelist=[e for e in dotted_edges if e in edge_colors],
                               edge_color=[edge_colors[e] for e in dotted_edges if e in edge_colors], style='dashed', width=1, alpha=0.7)
    # Draw all nodes
    nx.draw_networkx_nodes(G, pos=node_positions, node_size=20, node_color='blue')
    # Draw the start and goal nodes
    nx.draw_networkx_nodes(G, pos=node_positions, nodelist=[start_node], node_size=50, node_color='green')
    nx.draw_networkx_nodes(G, pos=node_positions, nodelist=[goal_node], node_size=50, node_color='red')
    plt.axis('off')

# Animate the path
animation = FuncAnimation(fig, update, frames=len(path_edges) + 1, interval=1, repeat=False)
plt.show()

