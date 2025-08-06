import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.id_map = {}  # Map vector index to message

    def add(self, message_id, embedding):
        vec = np.frombuffer(embedding, dtype=np.float32)
        idx = self.index.ntotal
        self.index.add(vec.reshape(1, -1))
        self.id_map[idx] = message_id

    def search(self, embedding, top_k=5):
        vec = np.frombuffer(embedding, dtype=np.float32).reshape(1, -1)
        distances, indices = self.index.search(vec, top_k)
        return [self.id_map[i] for i in indices[0] if i in self.id_map]
