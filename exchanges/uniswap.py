from .exchange import Exchange, Pair
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class Uniswap(Exchange):
    def fetch_pairs(self):
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")

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
                symbol
                }
                token1 {
                id
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
                token1=pair['token1']['symbol'],
                exchange="uniswap",
                price=float(pair['token1Price'])
            )
            yield Pair(
                token0=pair['token1']['symbol'],
                token1=pair['token0']['symbol'],
                exchange="uniswap",
                price=float(pair['token0Price'])
            )