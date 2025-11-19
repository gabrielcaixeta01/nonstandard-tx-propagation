# Non-standard Transaction Propagation in Filtering Bitcoin Networks

This repository contains the experimental setup and code for the project:

> **Simulate how easy it is to propagate non-standard transactions with filtering nodes.**

The goal is to empirically measure how *consensus-valid but policy-non-standard* Bitcoin transactions behave inside a mixed network where the majority of nodes enforce strict relay policies, and a minority accept or relay non-standard transactions.

---

## 1. Motivation

Bitcoin nodes operate under two distinct sets of rules:

- **Consensus rules** — determine which transactions and blocks are *valid*.
- **Policy rules** — determine which transactions nodes are *willing to relay or accept into their mempool*.

Therefore, some transactions:
- ✔ are **valid under consensus**, but  
- ✖ are **rejected by default node policy** (non-standard).

These transactions *could* be mined if a miner includes them in a block, but they rarely propagate through the network due to filtering rules.

This project investigates:

> **To what extent can non-standard (but consensus-valid) transactions propagate through a realistic Bitcoin-like network?**

---

## 2. Objective

The objective of this work is to:

- Generate several types of consensus-valid but non-standard transactions.
- Broadcast them across a simulated network that mixes filtering and permissive nodes.
- Measure how far these transactions travel (number of hops and nodes reached).
- Compare propagation patterns depending on:
  - transaction type,
  - broadcasting node,
  - presence of permissive nodes,
  - network topology.

The output is an empirical characterization of how robust Bitcoin’s policy layer truly is.

---

## 3. Approach

The experiment proceeds in five stages:

### **1. Build a mixed-policy network**
Using a regtest/Warnet environment, configure:
- **Filtering nodes:** strict default policy  
- **Permissive nodes:** `acceptnonstdtxn=1`, looser relay rules  

A small fraction (≈30%) of permissive nodes is enough to test bridging effects.

---

### **2. Create consensus-valid but non-standard transactions**

Examples include:

1. **Oversized `OP_RETURN`**  
   - larger than the relay-policy limit  
   - but consensus-valid  

2. **Bare multisig outputs**  
   - valid by consensus  
   - non-standard template  

3. **Scripts with non-canonical pushes**  
   - valid execution  
   - rejected by policy  

4. **Weird custom script templates**  
   - do not match P2PKH / P2WPKH / P2SH patterns  
   - but still spendable  

Each transaction type is crafted via RPC or script-building tools.

---

### **3. Broadcast transactions from different nodes**

For each transaction type:

- Send once from a filtering node  
- Send once from a permissive node  
- Send once from a miner-connected node  

This reveals how origin affects propagation.

---

### **4. Collect relay and mempool information**

After each broadcast:
- Query every node’s mempool  
- Log which nodes accepted or rejected the transaction  
- Store snapshots for analysis  

This produces a dataset containing:
- node → {list of txids in mempool}
- timestamps
- propagation patterns

---

### **5. Analyze propagation**

Using Python tools, compute:

- **Propagation success rate**  
  (fraction of nodes that accepted the transaction)

- **Hop distance**  
  (minimum number of peers needed to reach each node)

- **Influence of permissive nodes**  
  (do they significantly increase reach?)

- **Transaction-type sensitivity**  
  (some non-standard types propagate better than others)

Outputs may include:
- CSV summaries  
- propagation heatmaps  
- per-type comparisons  
- hop-distribution graphs  

---

## 4. Research Questions

This project explores several questions:

1. *How restrictive is Bitcoin’s relay policy in practice?*  
2. *Can permissive nodes act as bridges that allow non-standard transactions to reach many others?*  
3. *Which non-standard transaction templates propagate the most?*  
4. *Do any non-standard transactions reach a miner’s mempool?*  
5. *What does this reveal about the separation between policy and consensus?*  

---

## 5. Types of Non-standard Transactions Tested

The project evaluates propagation of:

- Oversized `OP_RETURN` outputs  
- Bare multisig scripts  
- Non-canonical push scripts  
- Custom script templates valid under consensus  
- High-sigops scripts close to the consensus threshold  

All are **consensus-valid**, but **policy-non-standard**.

---

## 6. Expected Findings

Based on prior documentation and anecdotal evidence, we anticipate:

- Most non-standard transactions **fail to propagate in a purely filtering network**.  
- Even a small number of permissive nodes can **significantly increase propagation**.  
- Bare multisig may propagate slightly better due to partial template matching.  
- Oversized `OP_RETURN` should propagate poorly.  
- Certain scripts may unexpectedly reach miner nodes depending on their policies.  

The goal is not to guess outcomes — but to measure them.

---
