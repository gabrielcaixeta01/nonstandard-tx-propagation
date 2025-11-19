# Node Policies for Non-standard Transaction Propagation Experiment

This document describes the policy settings used in the simulated Bitcoin network for the project:

> **Simulate how easy it is to propagate non-standard transactions with filtering nodes.**

The network contains two main categories of nodes:

- **Filtering nodes (default Bitcoin Core policy)**
- **Permissive nodes (relay and accept non-standard transactions)**

Additionally, there is one **miner node** that follows the default filtering policy.

---

## 1. Background: Consensus vs Policy

Bitcoin nodes apply two layers of rules:

### **Consensus rules**
- Define validity of blocks and transactions.
- Enforced by *all* nodes.
- Impossible to bypass without creating an invalid chain.

### **Policy rules**
- Local node-specific relay rules.
- Determine which transactions a node:
  - inserts into its mempool
  - relays to peers
- *Not* enforced by consensus.
- Can be overridden (not recommended on mainnet).

This experiment focuses on **policy-non-standard but consensus-valid** transactions.

---

## 2. Filtering Nodes (Default Policy)

Filtering nodes use Bitcoin Core’s default mempool policy.
These nodes:

- **Reject non-standard transactions**
- **Do not relay non-standard transactions**
- **Only accept transactions matching typical templates**, such as:
  - P2PKH
  - P2WPKH
  - P2SH
  - P2WSH
  - Taproot key-path spends

### Default policy settings:

acceptnonstdtxn=0
relaynonstandard=0
minrelaytxfee=0.00001
datacarriersize=80
permitbaremultisig=0

Filtering nodes are used to simulate the majority of the Bitcoin network.

### Filtering node behavior:
- Will immediately reject:
  - oversized OP_RETURN outputs
  - bare multisig scripts
  - non-canonical pushes
  - non-standard script templates
- Will not relay such transactions to peers
- Will not put them in mempool even if valid under consensus

14 out of 21 nodes in the network use filtering rules.

---

## 3. Permissive Nodes (Non-standard Relay Enabled)

These nodes are configured to **accept and relay non-standard transactions**.

They represent:
- experimental users,
- developers,
- special-purpose nodes,
- or hypothetical miners running permissive policy.

### Permissive policy settings:

acceptnonstdtxn=1
relaynonstandard=1
minrelaytxfee=0.00001
datacarriersize=100000   # allow large OP_RETURN
permitbaremultisig=1

### Permissive node behavior:
- Accept non-standard scripts into mempool
- Relay them to peers (even if peers later reject)
- Act as “bridges” across the network
- Allow propagation of unusual or experimental transactions

6 out of 21 nodes follow permissive rules.

---

## 4. Miner Node

The miner node uses **default (filtering) policy**, not permissive.

This allows us to test:
- Whether non-standard transactions *ever* reach a miner
- Whether permissive nodes are sufficient to push a transaction into a miner’s mempool
- How realistic mining behavior interacts with policy vs consensus

Miner settings:

acceptnonstdtxn=0
relaynonstandard=0
blockmintxfee=0.00001

The miner **will not mine** non-standard transactions *unless* they somehow reach its mempool.

---

## 5. Summary Table

| Node Type         | Count | acceptnonstdtxn | relaynonstandard | Behavior                                  |
|------------------|-------|-----------------|------------------|--------------------------------------------|
| Filtering Nodes  | 14    | 0               | 0                | Reject + don't relay non-standard tx       |
| Permissive Nodes | 6     | 1               | 1                | Accept + relay non-standard tx             |
| Miner Node       | 1     | 0               | 0                | Mines only standard tx unless relayed in   |

---

## 6. Why This Policy Mix?

The mix of filtering and permissive nodes allows us to answer:

- Do permissive nodes significantly increase propagation?
- How many hops can a non-standard transaction travel?
- Do relay policies “choke” non-standard transactions completely?
- Can a permissive node accidentally (or intentionally) push a non-standard tx into the wider network?
- How far does a consensus-valid but policy-invalid script survive?

This design mirrors real-world scenarios where:
- some nodes run modified policies (developers, researchers), but
- most nodes run default Bitcoin Core settings.

---

## 7. Example Non-standard Transactions Tested

The experiment includes:

1. **Oversized OP_RETURN**  
   - consensus-valid  
   - violates policy `datacarriersize`

2. **Bare multisig (2-of-2 or 3-of-3)**  
   - valid script  
   - rejected by `permitbaremultisig=0`

3. **Non-canonical ScriptPush**  
   - valid execution  
   - violates standard push rules

4. **Odd script templates**  
   - e.g., `OP_ADD OP_ADD OP_DROP` style  
   - consensus-valid  
   - policy-invalid

---

## 8. Implications

Understanding node policy behavior is crucial for:

- wallet design  
- layer-2 protocols  
- soft-fork activation strategies  
- privacy-enhancing scripts  
- experimental Bitcoin simulations  
- robustness of Bitcoin’s relay layer  

This file documents the precise node behavior that enables such experimentation.