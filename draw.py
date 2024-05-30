import matplotlib.pyplot as plt
import networkx as nx

def draw_neural_network(input_size, hidden_size, output_size):
    G = nx.DiGraph()

    # Adding nodes for each layer
    input_layer = ['Input_{}'.format(i+1) for i in range(input_size)]
    hidden_layer = ['Hidden_{}'.format(i+1) for i in range(hidden_size)]
    output_layer = ['Output_{}'.format(i+1) for i in range(output_size)]

    G.add_nodes_from(input_layer, layer='input')
    G.add_nodes_from(hidden_layer, layer='hidden')
    G.add_nodes_from(output_layer, layer='output')

    # Adding edges between layers
    for input_node in input_layer:
        for hidden_node in hidden_layer:
            G.add_edge(input_node, hidden_node)

    for hidden_node in hidden_layer:
        for output_node in output_layer:
            G.add_edge(hidden_node, output_node)

    pos = {}
    layer_distance = 1  # Distance between layers
    node_distance = 0.25  # Distance between nodes within each layer

    # Calculate vertical positions
    input_positions = [-i * node_distance for i in range(input_size)]
    hidden_positions = [-i * node_distance for i in range(hidden_size)]
    output_positions = [-i * node_distance for i in range(output_size)]

    # Center hidden layer positions
    hidden_start = (input_positions[-1] + input_positions[0]) / 2 - (hidden_positions[-1] + hidden_positions[0]) / 2
    hidden_positions = [pos + hidden_start for pos in hidden_positions]

    # Center output layer positions
    output_start = (input_positions[-1] + input_positions[0]) / 2 - (output_positions[-1] + output_positions[0]) / 2
    output_positions = [pos + output_start for pos in output_positions]

    # Positioning nodes
    pos.update((node, (0, input_positions[i])) for i, node in enumerate(input_layer))
    pos.update((node, (layer_distance, hidden_positions[i])) for i, node in enumerate(hidden_layer))
    pos.update((node, (2 * layer_distance, output_positions[i])) for i, node in enumerate(output_layer))

    # Drawing the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', font_size=8, font_weight='bold', arrows=True, arrowstyle='-|>', arrowsize=10, width=0.5)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={edge: '' for edge in G.edges()}, font_color='red')

    # Adding layer labels
    for layer, coords in [('Input Layer', (0, max(input_positions) + 0.25)), ('Hidden Layer (Sigmoid)', (layer_distance, max(input_positions) + 0.25)), ('Output Layer (Tanh)', (2 * layer_distance, max(input_positions) + 0.25))]:
        plt.text(coords[0], coords[1], layer, horizontalalignment='center', verticalalignment='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    plt.title('Compact Neural Network Diagram')
    plt.axis('off')
    plt.show()

# Parameters for the neural network
input_size = 20  # 16 sensors + 4 feedback
hidden_size = 4
output_size = 6

draw_neural_network(input_size, hidden_size, output_size)
