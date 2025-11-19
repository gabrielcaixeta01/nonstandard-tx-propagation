# src/utils.py

import json
import requests

class RPC:
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth

    def call(self, method, params=None):
        payload = {
            "jsonrpc": "1.0",
            "id": "rpc",
            "method": method,
            "params": params or []
        }
        r = requests.post(self.url, auth=self.auth, json=payload)
        r.raise_for_status()
        return r.json()["result"]

    def __getattr__(self, method):
        def wrapper(*params):
            return self.call(method, list(params))
        return wrapper


def get_rpc_clients():
    """
    Loads RPC connection info based on a static mapping of nodes.
    Modify rpc_port according to your Warnet setup.
    """
    nodes = {}

    # Miner
    nodes["miner-1"] = RPC(
        url="http://127.0.0.1:18443",
        auth=("user", "password")
    )

    # Filtering nodes
    for i in range(1, 15):
        nodes[f"node-filter-{i}"] = RPC(
            url=f"http://127.0.0.1:{18500+i}",
            auth=("user", "password")
        )

    # Permissive nodes
    for i in range(1, 7):
        nodes[f"node-perm-{i}"] = RPC(
            url=f"http://127.0.0.1:{18700+i}",
            auth=("user", "password")
        )

    return nodes