"""
Nexus Oracle Indexer — Build ChromaDB from NEXUS PRIME documentation
Runs in ephemeral container with --memory=4g limit
Processes all .md files, chunks them, embeds with sentence-transformers
"""

import os
import glob
import logging
import hashlib

import chromadb
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("nexus_indexer")

# ── Configuration ──────────────────────────────────────────────
DOCS_PATH = os.getenv("DOCS_PATH", "/workspace")
CHROMA_PATH = os.getenv("CHROMA_PATH", "/data/rag/chromadb")
COLLECTION_NAME = "nexus_docs"
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")

# Directories to skip during indexing
SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".next", "dist", "build",
    "data", "nexus_prime_backups", ".venv", "venv", "env",
    "npm_data", "npm_letsencrypt", "db_data", "redis_data",
    "ollama", "open-webui", "n8n_data",
}


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks


def should_skip(path: str) -> bool:
    """Check if path contains any skip directory."""
    parts = path.split(os.sep)
    return any(p in SKIP_DIRS for p in parts)


def compute_doc_id(source: str, chunk_idx: int) -> str:
    """Generate a deterministic ID for a document chunk."""
    raw = f"{source}::chunk_{chunk_idx}"
    return hashlib.md5(raw.encode()).hexdigest()


def index_documents():
    """Main indexing pipeline."""
    logger.info(f"Starting indexer — scanning {DOCS_PATH} for .md files")
    logger.info(f"Embedding model: {EMBED_MODEL}")
    logger.info(f"Chunk size: {CHUNK_SIZE}, overlap: {CHUNK_OVERLAP}")

    # 1. Find all .md files
    pattern = os.path.join(DOCS_PATH, "**", "*.md")
    all_files = glob.glob(pattern, recursive=True)
    md_files = [f for f in all_files if not should_skip(f)]

    logger.info(f"Found {len(all_files)} total .md files, {len(md_files)} after filtering")

    if not md_files:
        logger.error("No .md files found. Check DOCS_PATH.")
        return

    # 2. Load embedding model
    logger.info(f"Loading embedding model: {EMBED_MODEL} ...")
    model = SentenceTransformer(EMBED_MODEL)
    logger.info("Embedding model loaded.")

    # 3. Process files into chunks
    all_chunks = []
    all_metadatas = []
    all_ids = []

    for filepath in md_files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            if len(content.strip()) < 50:
                continue

            relative_path = os.path.relpath(filepath, DOCS_PATH)
            chunks = chunk_text(content)

            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadatas.append({
                    "source": relative_path,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                })
                all_ids.append(compute_doc_id(relative_path, i))

        except Exception as e:
            logger.warning(f"Error reading {filepath}: {e}")

    logger.info(f"Total chunks: {len(all_chunks)} from {len(md_files)} files")

    if not all_chunks:
        logger.error("No chunks generated. Aborting.")
        return

    # 4. Embed all chunks
    logger.info("Generating embeddings (this may take a few minutes)...")
    embeddings = model.encode(all_chunks, show_progress_bar=True, batch_size=32)
    logger.info(f"Embeddings generated: {embeddings.shape}")

    # 5. Store in ChromaDB
    logger.info(f"Writing to ChromaDB at {CHROMA_PATH}...")
    os.makedirs(CHROMA_PATH, exist_ok=True)

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Delete existing collection if it exists (full rebuild)
    try:
        client.delete_collection(COLLECTION_NAME)
        logger.info(f"Deleted existing collection '{COLLECTION_NAME}'")
    except ValueError:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "NEXUS PRIME documentation knowledge base"},
    )

    # Add in batches to avoid memory spikes
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        end = min(i + batch_size, len(all_chunks))
        collection.add(
            documents=all_chunks[i:end],
            embeddings=embeddings[i:end].tolist(),
            metadatas=all_metadatas[i:end],
            ids=all_ids[i:end],
        )
        logger.info(f"  Added batch {i//batch_size + 1}/{(len(all_chunks) + batch_size - 1)//batch_size}")

    final_count = collection.count()
    logger.info(f"✅ Indexing complete: {final_count} documents in '{COLLECTION_NAME}'")
    logger.info(f"   ChromaDB stored at: {CHROMA_PATH}")


if __name__ == "__main__":
    index_documents()
