"""
FILE: build_embeddings.py
CREATED: 2025-11-04 20:08:56
DESCRIPTION: Build sentence-transformer embeddings (CPU-friendly) over PatternForge datasets (.jsonl).
DEPENDENCIES: datasets, sentence_transformers, faiss-cpu
LOGGING: YYYY-MM-DD HH:MM:SS - build_embeddings - message
"""
import argparse, json, os
from pathlib import Path
from datetime import datetime

SCRIPT_NAME = "build_embeddings"

def log(msg): print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {SCRIPT_NAME} - {msg}")

def load_jsonl(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            yield json.loads(line)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(Path(__file__).resolve().parents[1] / "data/pattern_dataset.jsonl"))
    ap.add_argument("--out-index", default=str(Path(__file__).resolve().parents[1] / "data/patterns.faiss"))
    ap.add_argument("--out-meta", default=str(Path(__file__).resolve().parents[1] / "data/patterns.meta.jsonl"))
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np

    inp = Path(args.input)
    if not inp.exists():
        log(f"Input not found: {inp}")
        raise SystemExit(1)

    model = SentenceTransformer(args.model, device="cpu")
    log(f"Loaded encoder: {args.model}")

    texts, meta = [], []
    for rec in load_jsonl(inp):
        text = (rec.get("input","") + "\n\n" + rec.get("output","")).strip()
        if not text:
            continue
        texts.append(text)
        meta.append(rec)

    log(f"Encoding {len(texts)} texts... (CPU)")
    embs = model.encode(texts, batch_size=64, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=True)

    d = embs.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embs.astype("float32"))
    faiss.write_index(index, args.out_index)

    with open(args.out_meta, "w", encoding="utf-8") as f:
        for m in meta:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    log(f"Wrote index: {args.out_index} and meta: {args.out_meta}")

if __name__ == "__main__":
    main()
