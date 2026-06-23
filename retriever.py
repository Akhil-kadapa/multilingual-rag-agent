from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def retrieve_chunks(question, index, chunks, top_k=3):
    """
    Finds most relevant chunks for a question
    """
    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding).astype('float32')
    distances, indices = index.search(question_embedding, top_k)
    
    results = []
    for idx, i in enumerate(indices[0]):
        if i < len(chunks):
            chunk = chunks[i].copy()
            chunk['distance'] = float(distances[0][idx])
            results.append(chunk)

    results.sort(key=lambda x: x['distance'])
    filtered = [r for r in results if r['distance'] < 2.0]
    return filtered if filtered else results[:1]