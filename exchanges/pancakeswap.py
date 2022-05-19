from .exchange import Exchange, Pair
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import requests

class Pancakeswap(Exchange):
    def fetch_pairs(self):
        response = requests.get("https://api.pancakeswap.info/api/v2/pairs").json()
        pairs = response["data"].values()
        for pair in pairs:
            yield Pair(
                token0=pair['base_symbol'],
                token0_name=pair['base_name'],
                token1=pair['quote_symbol'],
                token1_name=pair['quote_name'],
                exchange="pancakeswap",
                price=float(pair['price'])
            )