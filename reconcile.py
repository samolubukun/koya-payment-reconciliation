#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

latest_by_txn = {}

with open("payments.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except Exception:
            continue

        if not isinstance(event, dict):
            continue

        txn_id = event.get("txn_id")
        if not txn_id:
            continue

        ts = event.get("ts")
        if not ts:
            continue

        existing = latest_by_txn.get(txn_id)
        if existing is None or ts > existing["ts"]:
            latest_by_txn[txn_id] = event

total = 0.0
count = 0

for event in latest_by_txn.values():
    if event.get("status") == "success":
        count += 1
        raw_amt = event.get("amount", 0)
        if isinstance(raw_amt, str):
            amt = float(raw_amt.replace(",", "").strip())
        else:
            amt = float(raw_amt)
        total += amt

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
