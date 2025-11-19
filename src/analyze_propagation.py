# src/analyze_propagation.py

import json
from pathlib import Path
import pandas as pd

RAW = Path("results/raw")
OUT = Path("results/processed")

def compute(df):
    rows = []
    for node, txids in df.items():
        for t in txids:
            rows.append({"node": node, "txid": t})
    df = pd.DataFrame(rows)
    if df.empty:
        print("No TXs found.")
        return None
    return df.groupby("txid").count().rename(columns={"node": "nodes_seen"})

def main():
    OUT.mkdir(parents=True, exist_ok=True)

    latest = sorted(RAW.glob("*/snapshot.json"))[-1]
    print("Using snapshot:", latest)

    with open(latest) as f:
        snap = json.load(f)

    df = compute(snap)
    if df is None:
        return

    outpath = OUT / "propagation_summary.csv"
    df.to_csv(outpath)
    print("Saved:", outpath)

if __name__ == "__main__":
    main()