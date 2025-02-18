import duckdb
import numpy as np

def init_database(database_name):
    # Connect (creates a file-based database)
    conn = duckdb.connect(database_name)

    # Create table with vector support
    conn.execute("""
        CREATE TABLE IF NOT EXISTS text_embeddings (
            chunk_id TEXT
            text_chunk TEXT,
            embedding FLOAT[768]  -- Native array support!
        )
    """)
    return conn

def add_to_database(conn,chunk,embedding):
    conn.execute("INSERT INTO text_embeddings (text_chunk, embedding) VALUES (?, ?)", (chunk, embedding))

# Initialize the database
conn = init_database("chunk_database")

# Insert an embedding safely
text = "Sensitive document"
embedding = np.random.rand(768).tolist()
add_to_database(conn,text,embedding)

# Query data
print(conn.execute("SELECT * FROM text_embeddings").fetchall())
