#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# run_experiment.sh
#
# Full pipeline to:
# 1. Start Warnet/regtest network
# 2. Generate non-standard transactions
# 3. Broadcast them from chosen nodes
# 4. Collect mempool snapshots from each node
# 5. Run propagation analysis
#
# All results stored under results/raw/ and results/processed/
###############################################################################

echo "=========================================================="
echo "  Non-standard Transaction Propagation Experiment"
echo "=========================================================="
echo ""

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
RAW_DIR="results/raw/${TIMESTAMP}"
mkdir -p "$RAW_DIR"

###############################################################################
# 1. Launch the network
###############################################################################

echo "[1/5] Starting Warnet network..."
# NOTE: You may need to change this depending on your Warnet setup.
# Replace the line below with your actual Warnet invocation.
#
# Example:
# warnet up config/network_topology.yaml
#
# or, if using Kubernetes:
# kubectl apply -f config/network_topology.yaml
#

echo ">> (TODO) Start Warnet with: warnet up config/network_topology.yaml"
echo ""
sleep 1

###############################################################################
# 2. Generate Consensus-Valid, Non-Standard Transactions
###############################################################################

echo "[2/5] Generating non-standard transactions..."

python3 - << 'EOF'
from src.tx_templates import NonStandardTxFactory
from src.utils import get_rpc_clients

# Load RPC clients for the network
nodes = get_rpc_clients()

# Pick a funding node (any with UTXOs)
funding_node = nodes["node-filter-1"]

factory = NonStandardTxFactory(funding_node)

print("[*] Generating transactions...")

# Collect funding UTXOs (this script assumes node-filter-1 has funds)
utxos = funding_node.listunspent()
funding_utxo = utxos[0]

tx_hex_opreturn = factory.create_oversized_op_return(funding_utxo)
tx_hex_baremultisig = factory.create_bare_multisig(funding_utxo)
tx_hex_weird = factory.create_weird_script_template(funding_utxo)

with open("results/nonstd_txs.txt", "w") as f:
    f.write(tx_hex_opreturn + "\n")
    f.write(tx_hex_baremultisig + "\n")
    f.write(tx_hex_weird + "\n")

print("[*] Created 3 non-standard transactions:")
print("    - oversized OP_RETURN")
print("    - bare multisig")
print("    - non-standard script template")
EOF

echo ""
echo "Non-standard transactions saved to results/nonstd_txs.txt"
echo ""

###############################################################################
# 3. Broadcast transactions from multiple nodes
###############################################################################

echo "[3/5] Broadcasting transactions across the network..."

python3 - << EOF
from src.broadcast import broadcast_scenario
from src.utils import get_rpc_clients

nodes = get_rpc_clients()

# Select 3 broadcast nodes:
# 1 filter node, 1 permissive node, 1 miner
broadcast_nodes = [
    nodes["node-filter-2"],
    nodes["node-perm-1"],
    nodes["miner-1"],
]

# Load raw transactions to broadcast
with open("results/nonstd_txs.txt") as f:
    raw_txs = [line.strip() for line in f.readlines() if line.strip()]

broadcast_scenario(broadcast_nodes, raw_txs)
EOF

echo ""
echo "Broadcast complete."
echo ""

###############################################################################
# 4. Collect mempool snapshots from every node
###############################################################################

echo "[4/5] Collecting mempool snapshots for all nodes..."

python3 - << EOF
import json
from src.collect_logs import collect_network_state
from src.utils import get_rpc_clients

nodes = get_rpc_clients()

snapshot = collect_network_state(nodes)

outfile = "${RAW_DIR}/snapshot.json"
with open(outfile, "w") as f:
    json.dump(snapshot, f, indent=2)

print(f"[+] Snapshot saved to {outfile}")
EOF

echo ""
echo "Snapshots collected."
echo ""

###############################################################################
# 5. Run propagation analysis
###############################################################################

echo "[5/5] Running propagation analysis..."

python3 -m src.analyze_propagation

echo ""
echo "=========================================================="
echo "Experiment Complete"
echo "Results:"
echo "  Raw data      -> ${RAW_DIR}"
echo "  Processed     -> results/processed/"
echo "=========================================================="