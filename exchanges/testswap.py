from .exchange import Exchange, Pair

class Testswap(Exchange):
    def fetch_pairs(self):
        yield Pair(
            token0="USDC",
            token0_name="$$$",
            token1="KESHAV",
            token1_name="Keshav Coin",
            exchange="testswap",
            price=1,
        )
        yield Pair(
            token0="KESHAV",
            token0_name="Keshav Coin",
            token1="USDC",
            token1_name="$$$",
            exchange="testswap",
            price=1,
        )