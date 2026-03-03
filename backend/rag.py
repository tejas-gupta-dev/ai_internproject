import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("kb_index.faiss")

with open("kb_docs.pkl", "rb") as f:
    documents = pickle.load(f)

def retrieve(query, k=1):
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), k)
    return documents[I[0][0]]