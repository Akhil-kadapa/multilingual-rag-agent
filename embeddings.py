from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def create_embeddings(chunks):
    """
    Converts text chunks into embedding vectors
    """
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts)
    return embeddings

def store_embeddings(embeddings, chunks):
    """
    Stores embeddings in FAISS index
    """
    embeddings = np.array(embeddings).astype('float32')
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, chunks