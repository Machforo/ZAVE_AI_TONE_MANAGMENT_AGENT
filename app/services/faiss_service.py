import os, json, faiss, numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
FAISS_DIR = "faiss_index"
os.makedirs(FAISS_DIR, exist_ok=True)

def embed_text(text: str) -> np.ndarray:
    return model.encode([text])[0].astype("float32")

def get_paths(user_id):
    return os.path.join(FAISS_DIR, f"{user_id}.index"), os.path.join(FAISS_DIR, f"{user_id}_meta.json")

def load_index(user_id):
    path_idx, path_meta = get_paths(user_id)
    if os.path.exists(path_idx) and os.path.exists(path_meta):
        idx = faiss.read_index(path_idx)
        meta = json.load(open(path_meta))
    else:
        idx = faiss.IndexFlatL2(384)
        meta = []
    return idx, meta

def save_index(user_id, idx, meta):
    path_idx, path_meta = get_paths(user_id)
    faiss.write_index(idx, path_idx)
    json.dump(meta, open(path_meta, "w"))

def add_message_to_faiss(user_id: str, message_id: str, text: str):
    idx, meta = load_index(user_id)
    emb = embed_text(text)
    idx.add(np.array([emb]))
    meta.append({"message_id": message_id, "text": text})
    save_index(user_id, idx, meta)

def search_similar_messages(user_id: str, query_text: str, top_k: int = 5):
    idx, meta = load_index(user_id)
    if not meta:
        return []
    emb = np.array([embed_text(query_text)])
    D, I = idx.search(emb, top_k)
    return [meta[i] for i in I[0] if i < len(meta)]

generate_embedding = embed_text
