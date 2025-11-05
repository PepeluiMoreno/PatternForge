"""
FILE: eval_retrieval.py
CREATED: 2025-11-04 20:08:56
DESCRIPTION: Quick retrieval evaluation using held-out queries.
DEPENDENCIES: sentence_transformers, faiss-cpu
"""
import argparse, json
from pathlib import Path
from datetime import datetime

SCRIPT_NAME = "eval_retrieval"
def log(msg): print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {SCRIPT_NAME} - {msg}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-queries", default=None, help="JSON list of {'q': str, 'expected_id': str}")
    ap.add_argument("--index", default=str(Path(__file__).resolve().parents[1] / "data/patterns.faiss"))
    ap.add_argument("--meta", default=str(Path(__file__).resolve().parents[1] / "data/patterns.meta.jsonl"))
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--k", type=int, default=5)
    args = ap.parse_args()

    import faiss, numpy as np
    from sentence_transformers import SentenceTransformer

    meta = [json.loads(l) for l in open(args.meta, "r", encoding="utf-8")]
    id2pos = {m['id']: i for i, m in enumerate(meta)}

    enc = SentenceTransformer(args.model, device="cpu")
    index = faiss.read_index(args.index)

    evals = json.loads(Path(args.eval_queries).read_text(encoding="utf-8")) if args.eval_queries else []
    correct = 0
    for e in evals:
        qemb = enc.encode([e["q"]], normalize_embeddings=True, convert_to_numpy=True)
        scores, ids = index.search(qemb.astype("float32"), args.k)
        top_ids = ids[0].tolist()
        # success if expected_id is in top-k
        if e["expected_id"] in [meta[i]["id"] for i in top_ids]:
            correct += 1
    total = len(evals) if evals else 1
    acc = correct / total
    print(json.dumps({"accuracy_topk": acc, "total": total, "correct": correct}, indent=2))

if __name__ == "__main__":
    main()
