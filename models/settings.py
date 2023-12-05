import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIDIR = os.path.join(ROOT_DIR, "abies")
WALLETSDIR = os.path.join(ROOT_DIR, "data")

ETHER_WALLETS = os.path.join(WALLETSDIR, "private_keys.txt")

TOKEN_ABI_JSON = os.path.join(ABIDIR, "evm_token.json")
SYNCSWAP_ABI_JSON = os.path.join(ABIDIR, "router.json")
SYNCSWAPPOOL_ABI_JSON = os.path.join(ABIDIR, "pool.json")
SYNCSWAPVALUE_ABI_JSON = os.path.join(ABIDIR, "value.json")
MINT_ABI_JSON = os.path.join(ABIDIR, "zkpepe.json")
