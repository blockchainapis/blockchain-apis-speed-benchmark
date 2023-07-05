import json
import os
import time

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Tuple

from web3 import Web3
from tqdm import tqdm

from src.Runner import Runner

_ABI_FOLDER_PATH = os.path.join("src", "abi")
_ROUTER_ABI_PATH = os.path.join(_ABI_FOLDER_PATH, "RouterAbi.json")
_FACTORY_ABI_PATH = os.path.join(_ABI_FOLDER_PATH, "FactoryAbi.json")
_PAIR_ABI_PATH = os.path.join(_ABI_FOLDER_PATH, "PairAbi.json")

def _load_abi(path: str) -> Any:
    with open(path, "r") as f:
        return json.load(f)

class NodeRunner(Runner):
    """Run the program using an Ethereum node.
    
    This ethereum node does more blockchain calls than BlockchainAPIs because
    that is required to get some missing data, like the address of the pair.
    
    Attributes:
        _token_balances: A dictionary containing as key the address of the token and as value
                         the amount of the token owned. It is the exact same balance as inside of the config
        _weth_address: The address of the wrapped ETH token
        _w3: The Web3 instance that allow us to interact with the Blockchain ethereum node
        _factory_caller: The ContractCaller instance that allow us to interact with the factory. We can use
                         this caller in order to get address of the pair of the two tokens.
    """

    def __init__(self, token_balances: Dict[str, int], weth_address: str, http_rpc: str, router_address: str):
        self._token_balances = token_balances
        self._weth_address = weth_address
        self._w3 = Web3(Web3.HTTPProvider(http_rpc))
        self._router_caller = self._w3.eth.contract(address=router_address, abi=_load_abi(_ROUTER_ABI_PATH)).caller()
        self._factory_caller = self._w3.eth.contract(address=self._router_caller.factory(), abi=_load_abi(_FACTORY_ABI_PATH)).caller()

    def _get_selling_result(self, token_address: str) -> Tuple[int, float]:
        """Get the amount of tokens that we will get after selling token_amount of
        token_address in exchange of Ethereum

        :param token_address: The address of the token
        :type token_address: str
        :return: The amount of ETH that we will get after selling token_amount of token_address and the duration
        :rtype: Tuple[int, float]
        """
        start = time.time()
        # Do an RPC call to get the address of the pair
        pair_address = self._factory_caller.getPair(self._weth_address, token_address)
        if pair_address == "0x0000000000000000000000000000000000000000":
            raise Exception(f"Token at address: {token_address} is not paired with WETH, please remove the token and try again")
        pair_caller = self._w3.eth.contract(address=pair_address, abi=_load_abi(_PAIR_ABI_PATH)).caller()
        # Get the reserves of the pair
        reserves = pair_caller.getReserves()
        # Get the token0 because, if token0 is the weth address then we need to reverse
        # reserve_in and reserve_out from the getReserves call
        token0 = pair_caller.token0()
        reserve_in, reserve_out = reserves[0], reserves[1]
        # Reverse the reserves in case token0 is WETH, because reserve_in is the reserve
        # of the token that we are selling. In our case, we are selling the token at
        # address `token_address`
        if token0 == self._weth_address:
            reserve_in, reserve_out = reserve_out, reserve_in
        # Do a call to the router in order to get the amount out
        amount_out = self._router_caller.getAmountOut(self._token_balances[token_address], reserve_in, reserve_out)
        return amount_out, time.time() - start

    def get_name(self) -> str:
        return "blockchain"

    async def run(self) -> Tuple[List[str], List[int], List[int], List[float]]:
        tokens_to_do = list(self._token_balances.keys())
        with ThreadPoolExecutor() as executor:
            returned_balances = list(tqdm(executor.map(self._get_selling_result, tokens_to_do), total=len(tokens_to_do)))

        return (
            tokens_to_do,
            [self._token_balances[token] for token in tokens_to_do],
            [returned_balances[i][0] for i in range(len(tokens_to_do))],
            [returned_balances[i][1] for i in range(len(tokens_to_do))]
        )
