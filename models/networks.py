class Network:
    def __init__(self, 
            name: str, rpc: str, chain_id: int, coin_symbol: str, 
            explorer: str, symbol: str, need_gas: int, orbiter_address: str = None):
        self.name = name
        self.rpc = rpc
        self.chain_id = chain_id
        self.coin_symbol = coin_symbol
        self.scan = explorer
        self.orbiter_address = orbiter_address
        self.need_gas = need_gas
        self.symbol = symbol
        
    def __str__(self):
        return f'{self.name.upper()}'

ZkSync = Network(
    name='ZkSync',
    rpc='https://zksync-era.blockpi.network/v1/rpc/public	', 
    chain_id=324,
    coin_symbol='ETH',
    explorer='https://explorer.zksync.io/',
    orbiter_address='',
    need_gas=1000,
    symbol="ETHER",
)