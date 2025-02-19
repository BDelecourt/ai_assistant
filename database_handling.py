import duckdb
import numpy as np

def init_database(database_name):
    # Connect (creates a file-based database)
    conn = duckdb.connect(database_name)

    # Create table with vector support
    conn.execute("""
        CREATE TABLE IF NOT EXISTS text_embeddings (
            chunk_id TEXT,
            text_chunk TEXT,
            embedding FLOAT[384]  -- Native array support!
        )
    """)
    print(f"successfully initialized {database_name}")
    return conn

def add_to_database(conn,chunk_id,text_chunk,embedding):

    try:
        conn.execute("INSERT INTO text_embeddings (chunk_id,text_chunk, embedding) VALUES (?,?,?)", (chunk_id, text_chunk, embedding))
    except Exception as e:
        print(f"Error ! Could not add Chunk:{chunk_id} to the database because of:\n{e}")

        return False
    
    print(f"Successfully added Chunk:{chunk_id} to the database")
    return True

def get_chunks_by_ids(conn, chunk_ids):
    if not chunk_ids:
        return []
    
    query = "SELECT text_chunk FROM text_embeddings WHERE chunk_id IN ({})".format(
        ','.join(['?'] * len(chunk_ids))
    )
    
    results = conn.execute(query, chunk_ids).fetchall()
    return [chunk[0] for chunk in results]