import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def visualize_flow(tx_list):
    # 1. Initialize the Graph
    G = nx.DiGraph() # Directed Graph (Money moves in a direction)

    # 2. Add connections from your data
    for tx in tx_list:
        G.add_edge(tx['from'][:6], tx['to'][:6], weight=tx['value'])

    # 3. Draw the Web
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G) # Spreads out the nodes like a web
    
    # Draw Nodes and Edges
    nx.draw(G, pos, with_labels=True, node_color='skyblue', 
            node_size=2000, edge_color='gray', arrowsize=20)
    
    # Add 'Value' labels to the lines
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("🕸️ EtherPulse: Token Transfer Graph")
    print("🎨 Rendering the money flow map...")
    plt.show()

# Simulated data of a Whale moving money through 'Mixer' wallets
whale_data = [
    {'from': 'Whale_A', 'to': 'Wallet_1', 'value': 500},
    {'from': 'Wallet_1', 'to': 'Wallet_2', 'value': 250},
    {'from': 'Wallet_1', 'to': 'Wallet_3', 'value': 250},
    {'from': 'Wallet_2', 'to': 'Exchange', 'value': 240},
    {'from': 'Wallet_3', 'to': 'Exchange', 'value': 240},
]

if __name__ == "__main__":
    visualize_flow(whale_data)