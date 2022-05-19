from .exchange import Exchange, Pair
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class Honeyswap(Exchange):
    def fetch_pairs(self):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/kirkins/honeyswap")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query get {
            pairs {
                id
                token0 {
                    id
                    name
                    symbol
                }
                token1 {
                    id
                    name
                    symbol
                }
                token0Price
                token1Price
            }
        }

        """
        )
        result = client.execute(query)
        pairs = result["pairs"]
        for pair in pairs:
            yield Pair(
                token0=pair['token0']['symbol'],
                token0_name=pair['token0']['name'],
                token1=pair['token1']['symbol'],
                token1_name=pair['token1']['name'],
                exchange="honeyswap",
                price=float(pair['token1Price'])
            )
            yield Pair(
                token0=pair['token1']['symbol'],
                token0_name=pair['token1']['name'],
                token1=pair['token0']['symbol'],
                token1_name=pair['token0']['name'],
                exchange="honeyswap",
                price=float(pair['token0Price'])
            )