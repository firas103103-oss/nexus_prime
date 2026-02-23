"""
Nexus Oracle API — RAG-powered documentation assistant
Reads pre-built ChromaDB (built by indexer.py in ephemeral container)
Generates answers via Ollama (llama3.2:3b)
"""

import os
import logging
from contextlib import asynccontextmanager

import httpx
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nexus_oracle")

# ── Configuration ──────────────────────────────────────────────
CHROMA_PATH = os.getenv("CHROMA_PATH", "/data/rag/chromadb")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://nexus_ollama:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2:3b")
COLLECTION_NAME = "nexus_docs"
TOP_K = int(os.getenv("TOP_K", "5"))

# ── Global state ───────────────────────────────────────────────
chroma_collection = None
http_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ChromaDB on startup, cleanup on shutdown."""
    global chroma_collection, http_client

    # Open ChromaDB in read-only mode
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        chroma_collection = client.get_collection(COLLECTION_NAME)
        doc_count = chroma_collection.count()
        logger.info(f"ChromaDB loaded: {doc_count} documents in '{COLLECTION_NAME}'")
    except Exception as e:
        logger.warning(f"ChromaDB not ready (run indexer first): {e}")
        chroma_collection = None

    http_client = httpx.AsyncClient(timeout=120.0)

    yield

    if http_client:
        await http_client.aclose()


app = FastAPI(
    title="Nexus Oracle",
    description="RAG-powered NEXUS PRIME documentation assistant",
    version="1.0.0",
    lifespan=lifespan,
)


# ── Models ─────────────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str
    top_k: int = TOP_K


class QueryResponse(BaseModel):
    answer: str
    sources: list[dict]
    model: str


# ── Endpoints ──────────────────────────────────────────────────
@app.get("/health")
async def health():
    """Health check for Docker healthcheck."""
    return {
        "status": "healthy",
        "chromadb": chroma_collection is not None,
        "doc_count": chroma_collection.count() if chroma_collection is not None else 0,
    }


@app.post("/ask", response_model=QueryResponse)
async def ask(req: QueryRequest):
    """Answer a question using RAG over NEXUS PRIME documentation."""
    if chroma_collection is None:
        raise HTTPException(
            status_code=503,
            detail="Knowledge base not indexed yet. Run nexus_oracle_reindex.sh first.",
        )

    # 1. Retrieve relevant documents
    results = chroma_collection.query(
        query_texts=[req.question],
        n_results=req.top_k,
    )

    if not results["documents"] or not results["documents"][0]:
        raise HTTPException(status_code=404, detail="No relevant documents found.")

    # Build context from retrieved docs
    context_parts = []
    sources = []
    for i, (doc, meta) in enumerate(
        zip(results["documents"][0], results["metadatas"][0])
    ):
        context_parts.append(f"[Source {i+1}: {meta.get('source', 'unknown')}]\n{doc}")
        sources.append(
            {
                "file": meta.get("source", "unknown"),
                "chunk": i + 1,
                "distance": round(results["distances"][0][i], 4)
                if results.get("distances")
                else None,
            }
        )

    context = "\n\n---\n\n".join(context_parts)

    # 2. Generate answer via Ollama
    prompt = f"""You are Nexus Oracle, the AI documentation assistant for NEXUS PRIME.
Answer the question based ONLY on the provided context. If the answer is not in the context, say so.
Be concise and accurate. Reference source files when relevant.

CONTEXT:
{context}

QUESTION: {req.question}

ANSWER:"""

    try:
        response = await http_client.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 512},
            },
        )
        response.raise_for_status()
        answer = response.json().get("response", "No response generated.")
    except httpx.HTTPError as e:
        logger.error(f"Ollama error: {e}")
        raise HTTPException(status_code=502, detail=f"LLM backend error: {str(e)}")

    return QueryResponse(answer=answer, sources=sources, model=MODEL_NAME)


@app.get("/stats")
async def stats():
    """Return knowledge base statistics."""
    if chroma_collection is None:
        return {"status": "not_indexed", "doc_count": 0}

    return {
        "status": "ready",
        "doc_count": chroma_collection.count(),
        "collection": COLLECTION_NAME,
        "model": MODEL_NAME,
    }
