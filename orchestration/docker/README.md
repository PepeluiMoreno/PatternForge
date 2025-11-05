# Orchestration (n8n + Ollama + optional Qdrant)

## Quick start
```bash
cd orchestration/docker
cp .env.example .env
docker compose up -d        # n8n + ollama
# docker compose --profile rag up -d  # add qdrant + rag-helper
```

- n8n UI: http://localhost:5678
- Ollama API: http://localhost:11434
- Qdrant (optional): http://localhost:6333
- rag-helper (optional): http://localhost:8000

Your repo is mounted into `/repo` **inside n8n** so workflows can read/write generated files.

## Models with Ollama
Pull a model once inside the container or from host:
```bash
docker exec -it ollama ollama pull llama3.1
docker exec -it ollama ollama pull nomic-embed-text   # embeddings
```
Then configure your n8n workflows/nodes to call Ollama at `http://ollama:11434`.

## Profiles
- Default: n8n + ollama
- `rag` profile: adds Qdrant + rag-helper for vector search and retrieval.
```bash
docker compose --profile rag up -d
```
