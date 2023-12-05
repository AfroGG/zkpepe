import asyncio
import random

from web3 import AsyncWeb3

from utils import script_exceptions, abi_read, logger
from models import Network, TOKEN_ABI_JSON
from config import MAX_DELAY, MIN_DELAY, NEED_DELAY_ACT



class EtherClient:
    TOKEN_ABI: str = abi_read(TOKEN_ABI_JSON)
    
    def __init__(self, index: int, network: Network, private: str) -> None:
        self.index = index
        self.network = network
        self.rpc = network.rpc

        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(self.rpc))
        
        self.private_key = private
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.address = self.account.address

    @staticmethod
    def random_int(lst: list) -> int:
        return random.randint(lst[0], lst[1])
    
    @staticmethod
    def random_float(lst: list) -> int:
        return random.uniform(lst[0], lst[1])
    
    @script_exceptions
    async def wait_for_gas(self) -> int:
        while True:
            gas = await self.w3.eth.gas_price
            if gas / 1_000_000_000 > self.network.need_gas:
                await asyncio.sleep(10)
            return gas
        
    @script_exceptions
    async def native_balance(self) -> int:
        balance = await self.w3.eth.get_balance(self.address)
        
        return balance

    @script_exceptions
    async def token_balance(self, token_address: str) -> float:
        contract_instance = self.w3.eth.contract(
            address=self.w3.to_checksum_address(token_address), 
            abi=EtherClient.TOKEN_ABI
        )
        
        return await contract_instance.functions.balanceOf(self.address).call()

    @script_exceptions
    async def send_transaction(self, transaction: dict) -> str:
        sign_tx = self.account.sign_transaction(transaction)
        tx_hash = self.w3.to_hex(await self.w3.eth.send_raw_transaction(sign_tx.rawTransaction))
        reciept = await self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if NEED_DELAY_ACT:
            await asyncio.sleep(random.randint(MIN_DELAY, MAX_DELAY))
        
        logger.success(f"Acc.{self.index} | Transaction Hash: {self.network.scan}tx/{tx_hash}")
        return tx_hash
        
    @script_exceptions
    async def approve_token(self, token: str, contract_address: str) -> str: 
        contract_instance = self.w3.eth.contract(address=self.w3.to_checksum_address(token), abi=self.TOKEN_ABI)
        value = await self.token_balance(token)
        
        tx = await contract_instance.functions.approve(self.w3.to_checksum_address(contract_address), value).build_transaction({
            "gasPrice": await self.wait_for_gas(),
            "from": self.address,
            "nonce": await self.w3.eth.get_transaction_count(self.address),
            "value": 0,
        })
        
        return await self.send_transaction(tx)
    