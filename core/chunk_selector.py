import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class ChunkSelector:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def chunk_text(self, text: str, chunk_size: int = 250):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunks.append(" ".join(words[i:i+chunk_size]))
        return chunks

    def select_relevant_chunks(self, text: str, top_k: int = 3):
        chunks = self.chunk_text(text)
        if not chunks:
            return []

        queries = [
            "technical skills",
            "education degree university",
            "work experience job role",
            "project portfolio",
            "certifications"
        ]

        chunk_vecs = self.model.encode(chunks, show_progress_bar=False)
        query_vecs = self.model.encode(queries, show_progress_bar=False)

        selected = []
        for qv in query_vecs:
            sims = cosine_similarity([qv], chunk_vecs)[0]
            idx = int(np.argmax(sims))
            selected.append(chunks[idx])

        # Deduplicate while preserving order
        seen = set()
        unique_selected = []
        for c in selected:
            if c not in seen:
                unique_selected.append(c)
                seen.add(c)

        return unique_selected[:top_k]