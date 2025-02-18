
from sentence_transformers import SentenceTransformer


def generate_embedding(text_chunk,model_name='all-MiniLM-L6-v2'):
    # Load pre-trained model
    model = SentenceTransformer(model_name)

    # Generate embeddings
    embeddings = model.encode([text_chunk])
    return embeddings.flatten()