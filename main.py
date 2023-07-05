import asyncio
import os

from dotenv import load_dotenv

from src.BlockchainAPIsRunner import BlockchainAPIsRunner
from src.NodeRunner import NodeRunner
from src.utils import load_config


async def main():
    load_dotenv()
    config = load_config("config.yml")
    node_runner = NodeRunner(config["token-owned"],
                             config["common"]["weth-address"],
                             os.getenv("HTTP_RPC"),
                             config["node-config"]["router-address"])
    blockchain_apis_runner = BlockchainAPIsRunner(config["token-owned"],
                                                  config["common"]["weth-address"],
                                                  config["blockchain-apis-config"]["blockchain-id"],
                                                  config["blockchain-apis-config"]["exchange-id"],
                                                  os.getenv("BLOCKCHAIN_APIS_KEY"))

    time_spent_node = await node_runner.time_run()
    time_spend_blockchain_apis = await blockchain_apis_runner.time_run()

    print(f"Ethereum node: {time_spent_node} seconds\nBlockchain APIs: {time_spend_blockchain_apis} seconds")

if __name__ == "__main__":
    asyncio.run(main())
