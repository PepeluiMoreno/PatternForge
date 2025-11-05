"""
FILE: rag_serve_fastapi.py
CREATED: 2025-11-04 20:08:56
DESCRIPTION: Minimal FastAPI RAG service (CPU). Given a query, returns top-k pattern contexts.
DEPENDENCIES: fastapi, uvicorn[standard], sentence_transformers, faiss-cpu
RUN: uvicorn train.rag_serve_fastapi:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss, json, numpy as np

INDEX_PATH = Path(__file__).resolve().parents[1] / "data/patterns.faiss"
META_PATH = Path(__file__).resolve().parents[1] / "data/patterns.meta.jsonl"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

app = FastAPI(title="PatternForge RAG API")

with open(META_PATH, "r", encoding="utf-8") as f:
    META = [json.loads(line) for line in f]
INDEX = faiss.read_index(str(INDEX_PATH))
ENC = SentenceTransformer(MODEL_NAME, device="cpu")

class Query(BaseModel):
    q: str
    k: int = 5

@app.post("/search")
def search(query: Query):
    qemb = ENC.encode([query.q], normalize_embeddings=True, convert_to_numpy=True)
    scores, ids = INDEX.search(qemb.astype("float32"), query.k)
    ids = ids[0].tolist(); scores = scores[0].tolist()
    hits = [{"score": float(s), "record": META[i]} for s, i in zip(scores, ids)]
    return {"query": query.q, "hits": hits}
