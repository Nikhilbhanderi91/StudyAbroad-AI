from typing import List, Dict, Any, Optional
import numpy as np
from rag.embeddings import EmbeddingManager
from rag.vector_store import FAISSVectorStore
from utils.config import FAISS_INDEX_PATH, FAISS_METADATA_PATH

class RAGRetriever:
    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.vector_store = FAISSVectorStore.load(FAISS_INDEX_PATH, FAISS_METADATA_PATH)

    def retrieve_documents(self, query: str, top_k: int = 5, score_threshold: float = 0.25) -> List[Dict[str, Any]]:
        """
        Retrieves top-k semantically relevant chunks for a user query.
        """
        query_vec = self.embedding_manager.encode_query(query)
        results = self.vector_store.search(query_vec, top_k=top_k)
        
        filtered = [doc for doc in results if doc.get("similarity_score", 0.0) >= score_threshold]
        # Return fallback results if threshold filtered too aggressively
        return filtered if filtered else results[:top_k]

    def format_context_for_llm(self, documents: List[Dict[str, Any]]) -> str:
        """Formats retrieved chunks into clean markdown context for LLM prompt."""
        if not documents:
            return "No relevant documents found in knowledge base."
        
        context_blocks = []
        for i, doc in enumerate(documents, 1):
            source = doc.get("source_file", "Database")
            topic = doc.get("topic", "Information")
            score = doc.get("similarity_score", 0.0)
            text = doc.get("text", doc.get("content", ""))
            block = f"--- [Document {i}] ---\nTopic: {topic}\nSource: {source} (Relevance Score: {score:.3f})\nContent:\n{text}\n"
            context_blocks.append(block)
            
        return "\n".join(context_blocks)
