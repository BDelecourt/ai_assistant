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
        conn.execute("INSERT INTO text_embeddings (chunk_id,text_chunk, embedding) VALUES (?,?, ?)", (chunk_id, text_chunk, embedding))
    except Exception as e:
        print(f"Error ! Could not add Chunk:{chunk_id} to the database because of:\n{e}")

        return False
    
    print(f"Successfully added Chunk:{chunk_id} to the database")
    return True