from typing import Dict, TypedDict

Common = TypedDict("Common", {
    "weth-address": str
})

NodeConfig = TypedDict("NodeConfig", {
    "router-address": str
})

Config = TypedDict("Config", {
    # Token owned contains as key the address of the token and as value
    # the amount of the token inside of the wallet
    "token-owned": Dict[str, int],
    "common": Common,
    "node-config": NodeConfig
})


