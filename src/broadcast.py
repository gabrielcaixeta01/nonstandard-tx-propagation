# src/broadcast.py

def broadcast_from_node(rpc, raw_tx):
    try:
        txid = rpc.sendrawtransaction(raw_tx)
        print(f"[+] Broadcast OK: {txid}")
        return txid
    except Exception as e:
        print(f"[!] Broadcast failed: {e}")
        return None


def broadcast_scenario(nodes, raw_txs):
    """
    nodes: list of RPC clients
    raw_txs: list of raw tx hex
    """
    for i, raw in enumerate(raw_txs):
        node = nodes[i % len(nodes)]
        print(f"\nBroadcasting from node: {node}")
        broadcast_from_node(node, raw)