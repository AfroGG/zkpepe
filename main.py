import asyncio
import random

from src import ZkPepe
from config import MIN_DELAY_ACC, MAX_DELAY_ACC, NUM_THREADS
from models import ETHER_WALLETS, ZkSync
from utils import logger


with open(ETHER_WALLETS, "r") as file:
    evm_keys = [key.strip() for key in file]
    
    
async def run_script(index: int, private: str):
    client = ZkPepe(index, ZkSync, private)
    await client.claim_tokens()
    await client.swap_to_ether()
    
    
async def main():
    tasks = []
    for index, evm_private in enumerate(evm_keys, start=1):
        task = run_script(index, evm_private)
        tasks.append(task)

        if len(tasks) == NUM_THREADS:
            await asyncio.gather(*tasks)
            tasks.clear()

        time = random.randint(MIN_DELAY_ACC, MAX_DELAY_ACC)
        logger.debug(f"Sleeping {time} seconds between accs")
        await asyncio.sleep()
    
    if tasks:
        await asyncio.gather(*tasks)
        
        
        
if __name__ == '__main__':
    print(f'ZkSync Pepe Claim + Swap | Starting script\n' * 3)

    asyncio.run(main())
    
    print('\n\nThank you for using the software. </3\n')
    input('Press "ENTER" To Exit..')