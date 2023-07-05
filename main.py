import asyncio

from src.BlockchainAPIsRunner import BlockchainAPIsRunner
from src.NodeRunner import NodeRunner
from src.utils import load_config


async def main():
    config = load_config("config.yml")
    node_runner = NodeRunner()
    blockchain_apis_runner = BlockchainAPIsRunner()

    time_spent_node = await node_runner.time_run()
    time_spend_blockchain_apis = await blockchain_apis_runner.time_run()

    print(f"Ethereum node: {time_spent_node} seconds\nBlockchain APIs: {time_spend_blockchain_apis} seconds")

if __name__ == "__main__":
    asyncio.run(main())
