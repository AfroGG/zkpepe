from web3 import AsyncWeb3

class Token:
    def __init__(self, symbol: str, address: str, decimals: int, woofi: str) -> None:
        self.symbol = symbol
        self.token_address = AsyncWeb3.to_checksum_address(address)
        self.decimals = decimals
        self.woofi = woofi
        self.zeroaddr = '0x0000000000000000000000000000000000000000'
    def __str__(self):
        return f'{self.symbol.upper()}'

        
ETH = Token(
    symbol='ETH',
    address='0x5300000000000000000000000000000000000004',
    decimals=18,
    woofi='0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
)

USDC = Token(
    symbol='USDC',
    address="0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
    decimals=6,
    woofi='0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4',
)

WETH = Token(
    symbol='WETH',
    address="0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
    decimals=18,
    woofi='0x5300000000000000000000000000000000000004',
)