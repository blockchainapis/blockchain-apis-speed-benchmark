from concurrent.futures import ThreadPoolExecutor
import time

from typing import Dict, List, Tuple

from blockchainapis import BlockchainAPIsSync
from tqdm import tqdm

from src.Runner import Runner


class BlockchainAPIsSyncRunner(Runner):

    def __init__(self, token_balances: Dict[str, int],
                 weth_address: str,
                 blockchain: str,
                 exchange: str,
                 blockchain_apis_key: str):
        self._token_balances = token_balances
        self._weth_address = weth_address
        self._blockchain = blockchain
        self._exchange = exchange
        self._blockchain_apis = BlockchainAPIsSync(blockchain_apis_key)

    def run_one(self, token_address: str) -> Tuple[int, float]:
        """Do one API call to get the amount out for given token address

        :param token_address: The address of the token
        :type token_address: str
        :return: A tuple containing at first the amount out and as second the duration of the call
        :rtype: Tuple[int, float]
        """
        start = time.time()
        amounts_out = self._blockchain_apis.amount_out(
            self._blockchain,
            self._weth_address,
            token_address,
            self._token_balances[token_address],
            self._exchange
        )
        duration = time.time() - start
        return amounts_out[0].amountOut, duration

    def get_name(self) -> str:
        return "BlockchainAPIsSync"

    async def run(self) -> Tuple[List[str], List[int], List[int], List[float]]:
        tokens_to_do = list(self._token_balances.keys())
        with ThreadPoolExecutor() as executor:
            result = list(tqdm(executor.map(self.run_one, tokens_to_do), total=len(tokens_to_do)))
        return (
            tokens_to_do,
            [self._token_balances[token] for token in tokens_to_do],
            [result[i][0] for i in range(len(tokens_to_do))],
            [result[i][1] for i in range(len(tokens_to_do))]
        )
