from typing import Dict, TypedDict


Config = TypedDict("Config", {
    # Token owned contains as key the address of the token and as value
    # the amount of the token inside of the wallet
    "token-owned": Dict[str, int],
})
