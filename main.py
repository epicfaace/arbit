import networkx as nx
import matplotlib
import math
import concurrent.futures
from exchanges.testswap import Testswap
from exchanges.uniswap import Uniswap
from exchanges.pancakeswap import Pancakeswap
from exchanges.honeyswap import Honeyswap

FETCH = True
SAVE_IMAGE = False

FEE_RATIO = .997
# FEE_RATIO = 1.000000001

if FETCH:

    # Execute the query on the transport
    G=nx.DiGraph()
    exchanges = [Testswap, Uniswap, Pancakeswap, Honeyswap]
    def fetch_pairs(exchange):
        pairs = exchange().fetch_pairs()
        i = 0
        for pair in pairs:
            if pair.price == 0:
                continue
            G.add_node(pair.token0, name=pair.token0_name)
            G.add_node(pair.token1, name=pair.token1_name)
            G.add_edge(pair.token0, pair.token1, weight=-1 * math.log(pair.price * FEE_RATIO), price=pair.price, exchange=pair.exchange)
            i +=1
            # print(dict(token0=pair.token0, token1=pair.token1, weight=-1 * math.log(pair.price * FEE_RATIO), exchange=pair.exchange))
        print(f"Got {i} pairs from {exchange}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        futures = [executor.submit(fetch_pairs, exchange) for exchange in exchanges]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()

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

node_lookup = dict(G.nodes(data=True))

for node in ["USDC"]:#G.nodes():
    try:
        cycle = nx.find_negative_cycle(G, source=node)
        print("CYCLE FOUND!!!")
        total_factor = 1
        for (i, node) in enumerate(cycle):
            if i + 1 < len(cycle):
                edge_data = G.get_edge_data(node, cycle[i + 1])
                total_factor *= edge_data["price"] * FEE_RATIO
                print(node, node_lookup[node]["name"], edge_data["price"], edge_data["exchange"])
            else:
                print(node)
        print("total factor", total_factor)
    except nx.exception.NetworkXError:
        pass