import networkx as nx
import matplotlib
import math
from exchanges.uniswap import Uniswap

FETCH = True
SAVE_IMAGE = False

RATIO = .9999995
# RATIO = 1.000000001

if FETCH:

    # Execute the query on the transport
    G=nx.DiGraph()
    exchanges = [Uniswap]
    for exchange in exchanges:
        pairs = exchange().fetch_pairs()
        for pair in pairs:
            if pair.price == 0:
                continue
            G.add_node(pair.token0)
            G.add_node(pair.token1)
            G.add_edge(pair.token0, pair.token1, weight=-1 * math.log(pair.price * RATIO), exchange=pair.exchange)
            print(dict(token0=pair.token0, token1=pair.token1, weight=-1 * math.log(pair.price * RATIO), exchange=pair.exchange))

    print(G)
    nx.write_gml(G, "graph.gml")

else:
    G = nx.read_gml("graph.gml")

if SAVE_IMAGE:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    f = plt.figure(figsize=(50, 100))
    nx.draw(G, ax=f.add_subplot(111), with_labels=True)
    f.savefig("graph.png")

for node in G.nodes():
    try:
        cycle = nx.find_negative_cycle(G, source=node)
        print("CYCLE FOUND!!!")
        for (i, node) in enumerate(cycle):
            if i + 1 < len(cycle):
                edge_data = G.get_edge_data(node, cycle[i + 1])
                print(node, 2 ** (-1 * edge_data["weight"] ), edge_data["exchange"])
            else:
                print(node)
    except nx.exception.NetworkXError:
        pass