from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx, os
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
COLLECTION = "patternforge"

app = FastAPI(title="PatternForge RAG Helper")

def qdrant():
    return QdrantClient(url=QDRANT_URL)

@app.on_event("startup")
def ensure_collection():
    qc = qdrant()
    try:
        qc.get_collection(COLLECTION)
    except Exception:
        qc.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=qmodels.VectorParams(size=768, distance=qmodels.Distance.COSINE),
        )

class IngestItem(BaseModel):
    id: str
    text: str

@app.post("/ingest")
async def ingest(item: IngestItem):
    # 1) embed text via Ollama embeddings
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{OLLAMA_BASE}/api/embeddings", json={"model": EMBEDDING_MODEL, "prompt": item.text})
        if r.status_code != 200:
            raise HTTPException(status_code=500, detail=r.text)
        vec = r.json().get("embedding")
    if not vec:
        raise HTTPException(status_code=500, detail="No embedding returned")

    # 2) upsert into Qdrant
    qc = qdrant()
    qc.upsert(
        collection_name=COLLECTION,
        points=[qmodels.PointStruct(id=item.id, vector=vec, payload={"text": item.text})]
    )
    return {"ok": True}

class QueryReq(BaseModel):
    text: str
    top_k: int = 5

@app.post("/search")
async def search(req: QueryReq):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{OLLAMA_BASE}/api/embeddings", json={"model": EMBEDDING_MODEL, "prompt": req.text})
        if r.status_code != 200:
            raise HTTPException(status_code=500, detail=r.text)
        qvec = r.json().get("embedding")
    if not qvec:
        raise HTTPException(status_code=500, detail="No embedding returned")

    qc = qdrant()
    res = qc.search(collection_name=COLLECTION, query_vector=qvec, limit=req.top_k)
    return [{"id": p.id, "score": p.score, "text": p.payload.get("text")} for p in res]
