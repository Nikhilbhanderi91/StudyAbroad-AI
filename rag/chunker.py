from typing import List, Dict, Any

class DocumentChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Chunker with metadata preservation.
        Default chunk_size ~500 chars (approx 100-120 words), suitable for compact structured university/scholarship cards.
        Overlap of 50 chars ensures semantic continuity across sentences without diluting retrieval density.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, raw_documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunked_docs = []
        for doc in raw_documents:
            text = doc.get("content", "").strip()
            if not text:
                continue
            
            # If text is within reasonable single-chunk size, keep it unified to preserve complete facts
            if len(text) <= self.chunk_size * 1.5:
                chunk = dict(doc)
                chunk["chunk_id"] = f"{doc.get('document_id', 'doc')}_chunk_0"
                chunk["text"] = text
                chunked_docs.append(chunk)
            else:
                start = 0
                chunk_idx = 0
                while start < len(text):
                    end = min(start + self.chunk_size, len(text))
                    # Attempt to break at newline or space
                    if end < len(text):
                        split_pos = text.rfind('\n', start, end)
                        if split_pos == -1 or split_pos <= start:
                            split_pos = text.rfind(' ', start, end)
                        if split_pos > start:
                            end = split_pos

                    chunk_text = text[start:end].strip()
                    if chunk_text:
                        chunk = dict(doc)
                        chunk["chunk_id"] = f"{doc.get('document_id', 'doc')}_chunk_{chunk_idx}"
                        chunk["text"] = chunk_text
                        chunked_docs.append(chunk)
                        chunk_idx += 1
                    
                    if end >= len(text):
                        break
                    start = max(start + 1, end - self.chunk_overlap)

        return chunked_docs
