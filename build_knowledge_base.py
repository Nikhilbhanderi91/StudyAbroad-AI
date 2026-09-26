import os
import json
import time
from typing import List, Dict, Any, Optional
from pathlib import Path

from rag.document_loader import load_all_structured_documents
from rag.chunker import DocumentChunker
from rag.embeddings import EmbeddingManager
from rag.vector_store import FAISSVectorStore
from utils.config import (
    FAISS_INDEX_PATH,
    FAISS_METADATA_PATH,
    DOCUMENTS_CORPUS_PATH,
    EMBEDDING_MODEL_NAME
)

def build_complete_knowledge_base(force_rebuild: bool = False) -> FAISSVectorStore:
    """
    Ingests all datasets, chunks textual knowledge, embeds vectors, and saves FAISS index.
    """
    if not force_rebuild and FAISS_INDEX_PATH.exists() and FAISS_METADATA_PATH.exists():
        print(f"📦 Loading existing FAISS vector store from {FAISS_INDEX_PATH}...")
        return FAISSVectorStore.load()

    print("🚀 Building Knowledge Base from scratch...")
    start_time = time.time()

    # 1. Ingest Raw Documents
    raw_docs = load_all_structured_documents()
    print(f"📄 Loaded {len(raw_docs)} structured documents.")

    # Save raw corpus
    DOCUMENTS_CORPUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DOCUMENTS_CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_docs, f, indent=2, ensure_ascii=False)

    # 2. Chunk Documents
    chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
    chunked_docs = chunker.chunk_documents(raw_docs)
    print(f"🧩 Generated {len(chunked_docs)} semantic document chunks.")

    # 3. Generate Embeddings
    print(f"🧠 Generating embeddings using '{EMBEDDING_MODEL_NAME}'...")
    embed_manager = EmbeddingManager()
    texts = [doc.get("text", doc.get("content", "")) for doc in chunked_docs]
    embeddings = embed_manager.encode_texts(texts, show_progress_bar=True)

    # 4. Create and Save FAISS Vector Store
    vector_store = FAISSVectorStore()
    vector_store.add_documents(chunked_docs, embeddings)
    vector_store.save()

    elapsed = time.time() - start_time
    print(f"🎉 Knowledge Base built and indexed successfully in {elapsed:.2f} seconds!")
    return vector_store

if __name__ == "__main__":
    build_complete_knowledge_base(force_rebuild=True)
