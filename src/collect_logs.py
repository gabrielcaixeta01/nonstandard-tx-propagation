# src/collect_logs.py

def get_mempool_snapshot(rpc):
    return rpc.getrawmempool()

def collect_network_state(nodes):
    snapshot = {}
    for node_id, rpc in nodes.items():
        try:
            mem = rpc.getrawmempool()
            snapshot[node_id] = mem
        except Exception:
            snapshot[node_id] = []
    return snapshot