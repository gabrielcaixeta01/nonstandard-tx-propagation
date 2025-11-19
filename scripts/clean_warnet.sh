#!/usr/bin/env bash
set -euo pipefail

echo "[*] Cleaning Warnet / regtest state..."

rm -rf results/raw/*
rm -rf results/processed/*
rm -f results/nonstd_txs.txt

echo "[*] Done."