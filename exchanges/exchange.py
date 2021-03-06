from dataclasses import dataclass

@dataclass
class Pair:
    token0: str
    token0_name: str
    token1: str
    token1_name: str
    exchange: str
    price: float # price = token1 / token0 ratio

class Exchange:
    """
    A crypto exchange.
    """
    def fetch_pairs(self):
        """
        Fetches pairs. Should yield Pair objects.
        """
        raise NotImplementedError