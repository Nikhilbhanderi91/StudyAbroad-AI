import os
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import faiss

from utils.config import FAISS_INDEX_PATH, FAISS_METADATA_PATH, EMBEDDING_DIMENSION

class FAISSVectorStore:
    def __init__(self, dimension: int = EMBEDDING_DIMENSION):
        self.dimension = dimension
        self.index: faiss.IndexFlatIP = faiss.IndexFlatIP(dimension) # Cosine similarity since embeddings are normalized
        self.metadata: List[Dict[str, Any]] = []

    def add_documents(self, documents: List[Dict[str, Any]], embeddings: np.ndarray):
        """Adds embedded documents and metadata into the FAISS index."""
        if len(documents) != embeddings.shape[0]:
            raise ValueError(f"Documents count ({len(documents)}) does not match embeddings shape ({embeddings.shape[0]})")
        
        self.index.add(embeddings)
        self.metadata.extend(documents)

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """Searches the vector index and returns top_k matching documents with scores."""
        if self.index.ntotal == 0:
            return []
        
        scores, indices = self.index.search(query_vector, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            doc = dict(self.metadata[idx])
            doc["similarity_score"] = float(score)
            results.append(doc)
            
        return results

    def save(self, index_path: Path = FAISS_INDEX_PATH, metadata_path: Path = FAISS_METADATA_PATH):
        """Persists the FAISS index and metadata to disk."""
        index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(index_path))
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved FAISS index with {self.index.ntotal} records to {index_path}")

    @classmethod
    def load(cls, index_path: Path = FAISS_INDEX_PATH, metadata_path: Path = FAISS_METADATA_PATH) -> "FAISSVectorStore":
        """Loads a pre-computed FAISS index and its metadata JSON."""
        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError(f"FAISS index or metadata not found at {index_path} / {metadata_path}")
        
        store = cls()
        store.index = faiss.read_index(str(index_path))
        with open(metadata_path, "r", encoding="utf-8") as f:
            store.metadata = json.load(f)
        return store
