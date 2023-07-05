import asyncio
import time

from typing import Dict, List, Tuple

from blockchainapis import BlockchainAPIs

from src.Runner import Runner


class BlockchainAPIsRunner(Runner):

    def __init__(self, token_balances: Dict[str, int],
                 weth_address: str,
                 blockchain: str,
                 exchange: str,
                 blockchain_apis_key: str):
        self._token_balances = token_balances
        self._weth_address = weth_address
        self._blockchain = blockchain
        self._exchange = exchange
        self._blockchain_apis_key = blockchain_apis_key

    async def run_one(self, blockchain_apis: BlockchainAPIs, token_address: str) -> Tuple[int, float]:
        """Do one API call to get the amount out for given token address

        :param token_address: The address of the token
        :type token_address: str
        :return: A tuple containing at first the amount out and as second the duration of the call
        :rtype: Tuple[int, float]
        """
        start = time.time()
        amounts_out = await blockchain_apis.amount_out(
            self._blockchain,
            self._weth_address,
            token_address,
            self._token_balances[token_address],
            self._exchange
        )
        duration = time.time() - start
        return amounts_out[0].amountOut, duration

    async def run(self) -> Tuple[List[str], List[int], List[int], List[float]]:
        tasks = []
        tokens_to_do = list(self._token_balances.keys())
        async with BlockchainAPIs(self._blockchain_apis_key) as blockchain_apis:
            for token in tokens_to_do:
                tasks.append(asyncio.create_task(self.run_one(blockchain_apis, token)))
            result = await asyncio.gather(*tasks)
        return (
            tokens_to_do,
            [self._token_balances[token] for token in tokens_to_do],
            [result[i][0] for i in range(len(tokens_to_do))],
            [result[i][1] for i in range(len(tokens_to_do))]
        )
