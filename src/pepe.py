import os
import time
import random
import asyncio

import httpx
from eth_abi import abi

from client import EtherClient
from models import Network, SYNCSWAP_ABI_JSON, SYNCSWAPPOOL_ABI_JSON, SYNCSWAPVALUE_ABI_JSON, MINT_ABI_JSON
from utils import abi_read, logger, script_exceptions
from config import *

class ZkPepe(EtherClient):
    def __init__(self, index: int, network: Network, private: str) -> None:
        super().__init__(index, network, private)
        self.session = httpx.AsyncClient(headers={
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.zksyncpepe.com/airdrop',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'X-KL-saas-Ajax-Request': 'Ajax_Request',
            'sec-ch-ua-platform': '"Windows"',
        })
        
        self.claim_instance = self.w3.eth.contract(
            address=self.w3.to_checksum_address('0x95702a335e3349d197036Acb04BECA1b4997A91a'), 
            abi=abi_read(MINT_ABI_JSON)
        )
        self.swap_instance = self.w3.eth.contract(
            address=self.w3.to_checksum_address('0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295'), 
            abi=abi_read(SYNCSWAP_ABI_JSON)
        )
        self.pool_instance = self.w3.eth.contract(
            address=self.w3.to_checksum_address("0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb"), 
            abi=abi_read(SYNCSWAPPOOL_ABI_JSON)
        )
        
        self.zkpepe_addr = self.w3.to_checksum_address('0x7D54a311D56957fa3c9a3e397CA9dC6061113ab3')

    @script_exceptions
    async def claim_tokens(self):
        logger.info(f"Acc.{self.index} | Starting Claim Tokens")
        amount = await self.session.get(
            f'https://www.zksyncpepe.com/resources/amounts/{self.address.lower()}.json'
        )
        
        proof_response = await self.session.get(
            f'https://www.zksyncpepe.com/resources/proofs/{self.address.lower()}.json'
        )
        
        tx = await self.claim_instance.functions.claim(
            proof_response.json(), self.w3.to_wei(amount.json()[0], 'ether')
        ).build_transaction({
            'chainId': 324,
            "from": self.address,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
            "value": 0,
            'gasPrice': await self.w3.eth.gas_price,
        })
        
        await self.send_transaction(tx)
        
    @script_exceptions
    async def swap_to_ether(self):
        logger.info(f"Acc.{self.index} | Approving tokens for swap")
        await self.approve_token(self.zkpepe_addr, "0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295")


        logger.info(f"Acc.{self.index} | Preparing to Swap")
        
        steps = [{
            "pool": "0x76B39F4E0C6d66877f506bdA2041462760A68593",
            "data": abi.encode(["address", "address", "uint8"], [self.zkpepe_addr, self.address, 1]),
            "callback": "0x0000000000000000000000000000000000000000",
            "callbackData": "0x"
        }]


        path = [{
            "steps": steps,
            "tokenIn": self.zkpepe_addr,
            "amountIn": await self.token_balance(self.zkpepe_addr)
        }]

        value_contract = self.w3.eth.contract(
            address="0x76B39F4E0C6d66877f506bdA2041462760A68593",
            abi=abi_read(SYNCSWAPVALUE_ABI_JSON)
        )
        
        value_out = await value_contract.functions.getAmountOut(
            self.zkpepe_addr,
            await self.token_balance(self.zkpepe_addr),
            self.address
        ).call()
        
        tx = await self.swap_instance.functions.swap(
            path,
            value_out,
            int(time.time()) + 1000000
        ).build_transaction({
            'chainId': 324,
            "from": self.address,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
            "value": 0,
            'gasPrice': await self.w3.eth.gas_price,
        })
        
        await self.send_transaction(tx)
        
        await self.session.aclose()