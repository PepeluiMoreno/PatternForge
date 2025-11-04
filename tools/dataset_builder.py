"""
FILE: dataset_builder.py
CREATED: 2025-11-04 19:48:06
DESCRIPTION: Merge multiple JSON/JSONL datasets into a single JSONL with optional dedup and shuffling.
DEPENDENCIES: This script may interact with sibling tools in PatternForge/tools and expects project folders:
 - patterns/ (Markdown patterns)
 - backend/templates/ (Jinja2-style templates)
 - frontend/templates/ (Jinja2-style templates)

Logging follows the convention:
YYYY-MM-DD HH:MM:SS - SCRIPT_NAME - message
"""

import os
import json
import argparse
import random
from pathlib import Path
from datetime import datetime

SCRIPT_NAME = "dataset_builder"

def log(msg: str):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {SCRIPT_NAME} - {msg}")

def read_lines(path: Path):
    if path.suffix.lower() == ".jsonl":
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    elif path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            for rec in data:
                yield rec
        else:
            yield data
    else:
        raise ValueError(f"Unsupported file type: {path}")

def dedup(records, key="id"):
    seen = set()
    for r in records:
        k = r.get(key)
        if k is None:
            k = json.dumps(r, sort_keys=True)
        if k in seen:
            continue
        seen.add(k)
        yield r

def main():
    ap = argparse.ArgumentParser(description="Build a unified JSONL dataset from multiple sources")
    ap.add_argument("--input", "-i", action="append", required=True, help="Input JSON/JSONL paths")
    ap.add_argument("--out", "-o", default=str(Path(__file__).resolve().parents[1] / "data/dataset_merged.jsonl"))
    ap.add_argument("--shuffle", action="store_true", help="Shuffle output")
    ap.add_argument("--dedup-key", default="id", help="Key to deduplicate (default: id)")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    all_records = []
    for p in args.input:
        path = Path(p)
        if not path.exists():
            log(f"Skipping missing input: {path}")
            continue
        log(f"Reading: {path}")
        all_records.extend(list(read_lines(path)))

    log(f"Loaded {len(all_records)} records")
    records = list(dedup(all_records, key=args.dedup_key))
    log(f"After dedup: {len(records)} records")

    if args.shuffle:
        random.shuffle(records)
        log("Shuffled output")

    with open(out_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    log(f"Wrote dataset: {out_path}")

if __name__ == "__main__":
    main()
