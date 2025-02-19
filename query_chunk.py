import duckdb
import heapq
import numpy as np
import threading
from embeddings import generate_embedding

# Function to compute cosine similarity manually
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0
    
    return dot_product / (norm_vec1 * norm_vec2)

# Function to process a batch and update global heap
def process_batch(batch, user_embedding, k, heap_lock, most_similar_chunks):
    local_heap = []
    for chunk_id, embedding in batch:
        embedding = np.array(embedding)
        similarity = cosine_similarity(user_embedding, embedding)
        heapq.heappush(local_heap, (similarity, chunk_id))
        if len(local_heap) > k:
            heapq.heappop(local_heap)
    
    # Merge local heap with global heap safely
    with heap_lock:
        for item in local_heap:
            heapq.heappush(most_similar_chunks, item)
            if len(most_similar_chunks) > k:
                heapq.heappop(most_similar_chunks)

# Function to retrieve most similar chunks using batch processing and threading
def find_k_most_similar_chunk(user_input, conn, k, batch_size):
    user_embedding = generate_embedding(user_input)
    offset = 0
    most_similar_chunks = []
    heap_lock = threading.Lock()
    threads = []

    while True:
        # Fetch batch from database
        batch = conn.execute(
            "SELECT chunk_id, embedding FROM text_embeddings LIMIT ? OFFSET ?", 
            [batch_size, offset]
        ).fetchall()
        
        if not batch:
            break  # No more data to process
        
        # Process batch in a separate thread
        thread = threading.Thread(
            target=process_batch, 
            args=(batch, user_embedding, k, heap_lock, most_similar_chunks)
        )
        threads.append(thread)
        thread.start()
        
        offset += batch_size

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Sort final top-k results by similarity
    most_similar_chunks.sort(reverse=True, key=lambda x: x[0])
    return most_similar_chunks

# Example usage
conn = duckdb.connect("chunck_database.db")
user_input = "How many cards do we have on the table in codename"
most_similar = find_k_most_similar_chunk(user_input, conn, k=3, batch_size=15)

for similarity, chunk_id in most_similar:
    print(f"Chunk ID: {chunk_id}, Similarity: {similarity}")
