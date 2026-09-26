from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.config import EMBEDDING_MODEL_NAME

class EmbeddingManager:
    _instance = None
    _model = None

    def __new__(cls, model_name: str = EMBEDDING_MODEL_NAME):
        if cls._instance is None:
            cls._instance = super(EmbeddingManager, cls).__new__(cls)
            cls._model = SentenceTransformer(model_name)
        return cls._instance

    @property
    def model(self) -> SentenceTransformer:
        return self._model

    def encode_texts(self, texts: List[str], batch_size: int = 64, show_progress_bar: bool = False) -> np.ndarray:
        """
        Generates dense vector embeddings.
        Returns L2-normalized float32 numpy array for cosine similarity matching via Inner Product index.
        """
        embeddings = self._model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        return embeddings.astype('float32')

    def encode_query(self, query: str) -> np.ndarray:
        """Encodes a single query string into a normalized 1D float32 vector."""
        embedding = self._model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        return embedding.astype('float32')
