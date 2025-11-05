"""
FILE: rag_infer.py
CREATED: 2025-11-04 20:08:56
DESCRIPTION: CPU-only RAG inference over FAISS index for PatternForge patterns.
DEPENDENCIES: sentence_transformers, faiss-cpu, transformers (for a small CPU LM), or just returns retrieved contexts.
"""
import argparse, json
from pathlib import Path
from datetime import datetime

SCRIPT_NAME = "rag_infer"
def log(msg): print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {SCRIPT_NAME} - {msg}")

def load_meta(meta_path: Path):
    with open(meta_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default=str(Path(__file__).resolve().parents[1] / "data/patterns.faiss"))
    ap.add_argument("--meta", default=str(Path(__file__).resolve().parents[1] / "data/patterns.meta.jsonl"))
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--query", required=True)
    args = ap.parse_args()

    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer

    index = faiss.read_index(args.index)
    meta = load_meta(Path(args.meta))
    enc = SentenceTransformer(args.model, device="cpu")

    q = enc.encode([args.query], normalize_embeddings=True, convert_to_numpy=True)
    scores, ids = index.search(q.astype("float32"), args.k)
    ids = ids[0].tolist(); scores = scores[0].tolist()

    hits = [{"score": float(s), "record": meta[i]} for s, i in zip(scores, ids)]
    print(json.dumps({"query": args.query, "hits": hits}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
