import time

from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Tuple

from tqdm import tqdm

from src.Runner import Runner


class NodeRunner(Runner):
    """Run the program using an Ethereum node.
    
    This ethereum node does more blockchain calls than BlockchainAPIs because
    that is required to get some missing data, like the address of the pair.
    """

    def __init__(self, token_balances: Dict[str, int]):
        self._token_balances = token_balances

    def _get_selling_result(self, token_address: str) -> Tuple[int, float]:
        """Get the amount of tokens that we will get after selling token_amount of
        token_address in exchange of Ethereum

        :param token_address: The address of the token
        :type token_address: str
        :return: The amount of ETH that we will get after selling token_amount of token_address and the duration
        :rtype: Tuple[int, float]
        """

    async def run(self):
        tokens_to_do = list(self._token_balances.keys())
        with ThreadPoolExecutor() as executor:
            returned_balances = list(tqdm(executor.map(self._get_selling_result, tokens_to_do), total=len(tokens_to_do)))

        self.write_result(
            tokens_to_do,
            [self._token_balances[token] for token in tokens_to_do],
            [returned_balances[i][0] for i in range(len(tokens_to_do))],
            [returned_balances[i][1] for i in range(len(tokens_to_do))]
        )
