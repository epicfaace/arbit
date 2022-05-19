from .exchange import Exchange, Pair

class Testswap(Exchange):
    def fetch_pairs(self):
        yield Pair(
            token0="USDC",
            token1="KESHAV",
            exchange="testswap",
            price=1,
        )
        yield Pair(
            token0="KESHAV",
            token1="USDC",
            exchange="testswap",
            price=1,
        )