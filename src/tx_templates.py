# src/tx_templates.py

import os

class NonStandardTxFactory:
    def __init__(self, rpc):
        self.rpc = rpc

    def _funding_info(self, funding_utxo):
        return funding_utxo["txid"], funding_utxo["vout"], funding_utxo["amount"]

    # ----------------------------------------------------------
    # 1) Oversized OP_RETURN (non-standard but consensus-valid)
    # ----------------------------------------------------------
    def create_oversized_op_return(self, funding_utxo):
        txid, vout, amount = self._funding_info(funding_utxo)

        data = "41" * 200  # 200 bytes of data → non-standard
        op_return_script = f"6a{data}"

        outputs = {op_return_script: 0}

        rawtx = self.rpc.createrawtransaction(
            [{"txid": txid, "vout": vout}],
            {},
            0
        )

        # Add manual OP_RETURN
        tx = self.rpc.decoderawtransaction(rawtx)
        tx["vout"] = [{"value": 0, "scriptPubKey": {"hex": op_return_script}}]

        hex_tx = self.rpc.signrawtransactionwithwallet(rawtx)["hex"]
        return hex_tx

    # ----------------------------------------------------------
    # 2) Bare multisig (valid but non-standard)
    # ----------------------------------------------------------
    def create_bare_multisig(self, funding_utxo):
        txid, vout, amount = self._funding_info(funding_utxo)

        # Generate 2 new pubkeys
        pk1 = self.rpc.getnewaddress()
        pk2 = self.rpc.getnewaddress()

        p1 = self.rpc.getaddressinfo(pk1)["pubkey"]
        p2 = self.rpc.getaddressinfo(pk2)["pubkey"]

        # Bare multisig script
        script = f"5221{p1}21{p2}52ae"  # 2-of-2 multisig

        rawtx = self.rpc.createrawtransaction(
            [{"txid": txid, "vout": vout}],
            {},
            0
        )

        tx = self.rpc.decoderawtransaction(rawtx)
        tx["vout"] = [{"value": 0.00001, "scriptPubKey": {"hex": script}}]

        hex_tx = self.rpc.signrawtransactionwithwallet(rawtx)["hex"]
        return hex_tx

    # ----------------------------------------------------------
    # 3) Weird script template (valid but non-standard)
    # ----------------------------------------------------------
    def create_weird_script_template(self, funding_utxo):
        txid, vout, amount = self._funding_info(funding_utxo)

        # Push then drop — weird but valid
        script = "01020304 6d"  # push bytes then OP_DROP

        rawtx = self.rpc.createrawtransaction(
            [{"txid": txid, "vout": vout}],
            {},
            0
        )

        tx = self.rpc.decoderawtransaction(rawtx)
        tx["vout"] = [{"value": 0.00001, "scriptPubKey": {"hex": script}}]

        hex_tx = self.rpc.signrawtransactionwithwallet(rawtx)["hex"]
        return hex_tx